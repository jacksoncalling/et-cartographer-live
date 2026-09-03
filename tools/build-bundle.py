# -*- coding: utf-8 -*-
"""Emit a shared map.json bundle from a cartographer map folder.

Usage:
    python tools/build-bundle.py <map-folder>     (default: map)

Writes <map-folder>/map.json -- the single source of truth for both the frontend
and the shopkeeper backend.  Bundle includes:
  - nodes   full records: id, type, status, desc, movements text, source
  - edges   [[a, b], ...]
  - hero    most central ghost
  - topReal most central non-ghost
  - northStar
  - components   connected components (main first; islands labeled)
  - componentMap {node: component_index}

Graph construction is identical to build-artifact.py (same movements_zone rule,
same nav-node exclusion) so bundle graph == artifact graph.
"""
import os, json, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from graph_utils import split_fm, LINK, movements_zone, parse_body, brandes, connected_components

ROOT = os.path.join(HERE, "..")
MAPARG = sys.argv[1] if len(sys.argv) > 1 else "map"
MAP = os.path.join(ROOT, MAPARG)
CONFIG = os.path.join(MAP, "build.json")
if not os.path.isfile(CONFIG):
    raise SystemExit("no build.json in %s" % MAP)
cfg = json.load(open(CONFIG, encoding="utf-8"))
EXCLUDE = {"Catalog", "North Star"}

name = lambda p: os.path.splitext(os.path.basename(p))[0]
def read(p): return open(p, encoding="utf-8").read()

# ---- load ----
files = []
for root, _, fs in os.walk(MAP):
    for f in fs:
        if f.endswith(".md"): files.append(os.path.join(root, f))
allnodes = set(name(p) for p in files)
records = {}
north_star = ""
for p in files:
    nid = name(p)
    fm, body = split_fm(read(p))
    title, desc, hits, miss, source = parse_body(body)
    if nid == "North Star": north_star = desc or ""
    if nid in EXCLUDE or fm.get("type", "").lower() == "meta": continue
    mzone = movements_zone(body)
    connects = []
    for m in LINK.findall(mzone):
        t = m.strip()
        if t != nid and t in allnodes and t not in EXCLUDE and t not in connects:
            connects.append(t)
    records[nid] = dict(
        id=nid, label=nid,
        type=fm.get("type", "Object"),
        status=fm.get("status", "live").lower(),
        kind=fm.get("kind", ""),
        hub=fm.get("hub", ""),
        desc=desc,
        movements=mzone.strip(),
        hits=hits or "",
        doesNotHit=miss or "",
        source=source or "",
        connects=connects,
    )

# ---- graph ----
adj = defaultdict(set)
for nid, r in records.items():
    for t in r["connects"]:
        if t in records:
            adj[nid].add(t); adj[t].add(nid)
for nid in records: adj[nid]

# ---- betweenness + components ----
bet = brandes(adj)
comps = connected_components(adj)
comp_map = {n: i for i, c in enumerate(comps) for n in c}

ghosts = [(bet[n], n) for n, r in records.items() if r["status"] == "ghost"]
hero_bet, hero_id = max(ghosts) if ghosts else max((bet[n], n) for n in records)
real = [(bet[n], n) for n, r in records.items() if r["status"] != "ghost"]
top_bet, top_id = max(real) if real else (0.0, "")

maxbet = max(bet.values()) if bet else 0.0
def tier_of(b):
    frac = (b / maxbet) if maxbet else 0.0
    if frac >= 0.5: return "Load-bearing"
    if frac >= 0.2: return "Bridge"
    if frac > 0:    return "Connector"
    return "Leaf"

for nid, r in records.items():
    r["bet"] = round(bet.get(nid, 0.0), 1)
    r["tier"] = tier_of(bet.get(nid, 0.0))
    r["component"] = comp_map.get(nid, -1)

edges = []
seen = set()
for a in adj:
    for b in adj[a]:
        k = tuple(sorted((a, b)))
        if k not in seen: seen.add(k); edges.append(list(k))

bundle = dict(
    nodes=list(records.values()),
    edges=edges,
    hero=dict(id=hero_id, label=hero_id, bet=round(hero_bet, 1)),
    topReal=dict(id=top_id, label=top_id, bet=round(top_bet, 1)),
    northStar=north_star,
    components=[
        dict(index=i, nodes=c, size=len(c),
             island=(len(c) == 1),
             label=c[0] if len(c) == 1 else "main" if i == 0 else f"component-{i}")
        for i, c in enumerate(comps)
    ],
    componentMap=comp_map,
    openingGap=cfg.get("demo", {}).get("openingGap", ""),
)

out = os.path.join(MAP, "map.json")
json.dump(bundle, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"wrote {os.path.abspath(out)}")
print(f"nodes {len(records)}  edges {len(edges)}  components {len(comps)}")
print(f"hero ghost: {hero_id} {round(hero_bet,1)} | top real: {top_id} {round(top_bet,1)}")
