# -*- coding: utf-8 -*-
"""Build the walkable HTML cartography for one map folder.

Usage:
    python tools/build-artifact.py <map-folder>     (default: map)

Reads <map-folder>/build.json for the template, the output filename, and the
shelf rules. Parses the notes, computes betweenness + modularity on the OBJECT
graph (navigation nodes excluded), then injects the data into the template.

One builder, one graph rule, N territories. The only per-territory differences
(which template skin, what to name the output, how to shelve the nouns) live in
each map's build.json, not in this code.
"""
import os, re, json, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from graph_utils import split_fm, clean, LINK, movements_zone, parse_body, brandes, communities

ROOT = os.path.join(HERE, "..")
MAPARG = sys.argv[1] if len(sys.argv) > 1 else "map"
MAP = os.path.join(ROOT, MAPARG)
CONFIG = os.path.join(MAP, "build.json")
if not os.path.isfile(CONFIG):
    raise SystemExit("no build.json in %s (needs: template, out, shelves)" % MAP)
cfg = json.load(open(CONFIG, encoding="utf-8"))
TEMPLATE = os.path.join(HERE, cfg["template"])
OUT = os.path.join(ROOT, "output", cfg["out"])
SHELVES = cfg["shelves"]
REPO_BASE = cfg.get("repo_base", "").rstrip("/")
EXCLUDE = {"Catalog", "North Star"}

name = lambda p: os.path.splitext(os.path.basename(p))[0]
def read(p): return open(p, encoding="utf-8").read()

# A source citation is a chain of locators. Turn each URL and each internal
# path:line into a clickable link (path:line needs the map's repo_base). Plain
# text between locators is kept as-is, so a `verified:` stamp or a quote survives.
SRC_TOKEN = re.compile(
    r"(?P<url>https?://[^\s;)\]]+)"
    r"|(?P<path>[A-Za-z0-9_][A-Za-z0-9_./\-]*\.(?:py|md|json|ya?ml|html?|txt|js|ts|toml|cfg|csv|pdf))"
    r"(?::(?P<l1>\d+)(?:-(?P<l2>\d+))?)?")

def linkify_source(text):
    """Render a Source line as HTML with URLs and internal file:line locators as
    links. path:line resolves against REPO_BASE (e.g. a GitHub blob URL); with no
    repo_base the path stays plain text, still a valid citation, just not clickable."""
    if not text:
        return ""
    def repl(m):
        if m.group("url"):
            u = m.group("url").rstrip(".,;")
            return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, u)
        path, l1, l2 = m.group("path"), m.group("l1"), m.group("l2")
        label = m.group(0)
        if not REPO_BASE:
            return label
        frag = ""
        if l1:
            frag = "#L" + l1 + ("-L" + l2 if l2 else "")
        return '<a href="%s/%s%s" target="_blank" rel="noopener">%s</a>' % (
            REPO_BASE, path, frag, label)
    return SRC_TOKEN.sub(repl, text)

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
    if nid == "North Star": north_star = desc
    # Navigation / checkpoint nodes are never graph objects (matches gap-scan.py):
    # by filename, and by frontmatter type: meta (Catalog, North Star, Inventory).
    if nid in EXCLUDE or fm.get("type", "").lower() == "meta": continue
    connects = []
    mzone = movements_zone(body)
    for m in LINK.findall(mzone):
        t = m.strip()
        if t != nid and t in allnodes and t not in EXCLUDE and t not in connects:
            connects.append(t)
    records[nid] = dict(id=nid, label=nid, type=fm.get("type", "Object"),
                        status=fm.get("status", "live").lower(), kind=fm.get("kind", ""),
                        hub=fm.get("hub", ""), subtype=fm.get("subtype", "").lower(),
                        desc=desc, hits=hits, doesNotHit=miss, connects=connects,
                        source=linkify_source(source))

# ---- graph (object nodes only) ----
adj = defaultdict(set)
for nid, r in records.items():
    for t in r["connects"]:
        if t in records:
            adj[nid].add(t); adj[t].add(nid)
for nid in records: adj[nid]

bet = brandes(adj)
cof = communities(adj)
comm = defaultdict(list)
for n, c in cof.items(): comm[c].append(n)
ranked = sorted(comm.values(), key=lambda v: -len(v))
big = set(ranked[0]) if ranked else set()

def shelf(rec):
    """Apply the map's ordered shelf rules; first match wins, else Emergent.
    A rule is {"when": [[field, op, value], ...], "shelf": name}; ops are
    eq (equals), in (in a list), contains (substring). Conditions are ANDed."""
    fields = {
        "status":  rec["status"],
        "type":    rec["type"].lower(),
        "subtype": rec.get("subtype", ""),
        "kind":    rec["kind"].lower(),
        "hub":     rec["hub"].lower(),
    }
    fields["sub_or_kind"] = fields["subtype"] or fields["kind"]
    for rule in SHELVES:
        ok = True
        for f, op, val in rule.get("when", []):
            fv = fields.get(f, "")
            if op == "eq": ok = (fv == val)
            elif op == "in": ok = (fv in val)
            elif op == "contains": ok = (val in fv)
            else: ok = False
            if not ok: break
        if ok: return rule["shelf"]
    return "Emergent"

# hero = most central ghost
ghosts = [(bet[n], n) for n, r in records.items() if r["status"] == "ghost"]
hero_bet, hero_id = max(ghosts) if ghosts else max((bet[n], n) for n in records)

# plain-language reach tier: betweenness as a fraction of the map's busiest node.
maxbet = max(bet.values()) if bet else 0.0
def tier_of(b):
    frac = (b / maxbet) if maxbet else 0.0
    if frac >= 0.5: return "Load-bearing"
    if frac >= 0.2: return "Bridge"
    if frac > 0:    return "Connector"
    return "Leaf"

nodes = []
for nid, r in records.items():
    r = dict(r)
    r["bet"] = round(bet.get(nid, 0.0), 1)
    r["tier"] = tier_of(bet.get(nid, 0.0))
    r["cluster"] = 0 if nid in big else 1
    r["shelf"] = shelf(r)
    r["alert"] = (nid == hero_id)
    nodes.append(r)

edges = []
seen = set()
for a in adj:
    for b in adj[a]:
        k = tuple(sorted((a, b)))
        if k not in seen: seen.add(k); edges.append([k[0], k[1]])

real = [(bet[n], n) for n, r in records.items() if r["status"] != "ghost"]
top_bet, top_id = max(real) if real else (0.0, "")
DATA = dict(nodes=nodes, edges=edges,
            hero=dict(id=hero_id, label=hero_id, bet=round(hero_bet, 1)),
            topReal=dict(id=top_id, label=top_id, bet=round(top_bet, 1)),
            northStar=north_star,
            openingGap=cfg.get("demo", {}).get("openingGap", ""))

tpl = read(TEMPLATE)
html = tpl.replace("/*__DATA__*/", "const DATA = " + json.dumps(DATA, ensure_ascii=False) + ";")
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", os.path.abspath(OUT))
print("nodes", len(nodes), "edges", len(edges), "clusters", len(ranked))
print("hero ghost:", hero_id, round(hero_bet, 1), "| top real:", top_id, round(top_bet, 1))
print("shelves used:", sorted(set(n["shelf"] for n in nodes)))
