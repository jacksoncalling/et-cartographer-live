# -*- coding: utf-8 -*-
"""
gap-scan.py  --  the cheap InfraNodus for a cartographer map.

Runs on a map/ folder of the cartographer format (one note per object, links
written as [[wikilinks]], simple YAML frontmatter with type/status).

It reports:
  1. REAL HUBS      - betweenness centrality (navigation nodes excluded).
                      These are the true brokers, the load-bearing nodes.
  2. LOAD-BEARING   - ghost nodes ranked by betweenness. A ghost with high
     ABSENCE          centrality is a missing thing the whole structure leans on.
  3. CLUSTERS       - greedy-modularity communities (the natural worlds).
  4. STRUCTURAL     - cluster pairs that barely connect (the missing mycelium).
     GAPS

The algorithms are standard and need no tuning to be correct. The calibration
knobs (cluster resolution, gap threshold, link weighting) are meant to be set
AFTER looking at results on a real map, not in advance.

Usage:
    python gap-scan.py [path-to-map-folder]
Defaults to ../map relative to this file.
"""
import os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from graph_utils import split_fm, LINK, movements_zone, brandes, communities, connected_components, bfs_all

MAP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "map")

# ---- load notes ------------------------------------------------------------
files = []
for root, _, fs in os.walk(MAP):
    for f in fs:
        if f.endswith(".md"):
            files.append(os.path.join(root, f))
if not files:
    sys.exit("No .md notes found under: " + os.path.abspath(MAP))

name = lambda p: os.path.splitext(os.path.basename(p))[0]

# parse each file once: fm (lowercased values for is_nav/is_ghost checks) + body
parsed = {name(p): split_fm(open(p, encoding="utf-8").read()) for p in files}
meta   = {n: {k: v.lower() for k, v in fm.items()} for n, (fm, _) in parsed.items()}
bodies = {n: body for n, (_, body) in parsed.items()}

def is_nav(n):
    fm = meta.get(n, {})
    return fm.get("type") == "meta" or fm.get("role") == "front-door"
def is_ghost(n):
    return meta.get(n, {}).get("status") == "ghost"

# The object graph: navigation nodes (catalog, north star) are excluded from the
# graph itself, not just from the report. A table-of-contents node that links to
# everything would otherwise absorb the paths and distort every score.
nodes = set(n for n in parsed if not is_nav(n))
adj = defaultdict(set)

for s, body in bodies.items():
    if is_nav(s): continue
    mzone = movements_zone(body)
    for m in LINK.findall(mzone):
        t = m.strip()
        if t != s and t in nodes:
            adj[s].add(t); adj[t].add(s)
for n in nodes:
    adj[n]

# ---- betweenness (Brandes) -------------------------------------------------
bet = brandes(adj)

# ---- greedy modularity communities -----------------------------------------
cof = communities(adj)
comm = defaultdict(list)
for n, c in cof.items(): comm[c].append(n)
clusters = [sorted(v) for _, v in sorted(comm.items(), key=lambda kv: -len(kv[1]))]
cid = {n: i for i, c in enumerate(clusters) for n in c}

# ---- report ----------------------------------------------------------------
edges = sum(len(v) for v in adj.values()) // 2
print(f"map: {os.path.abspath(MAP)}")
print(f"nodes: {len(nodes)}   edges: {edges}\n")

print("=== REAL HUBS (betweenness; navigation nodes excluded) ===")
for n, v in sorted(bet.items(), key=lambda kv: -kv[1]):
    if is_nav(n) or v <= 0: continue
    print(f"  {v:7.1f}  {n}" + ("   [GHOST]" if is_ghost(n) else ""))

print("\n=== LOAD-BEARING ABSENCE (ghosts ranked by betweenness) ===")
gh = sorted([(bet[n], n) for n in nodes if is_ghost(n)], reverse=True)
if gh:
    for v, n in gh:
        print(f"  {v:7.1f}  {n}")
    print("  (a ghost high on this list is a missing thing the structure leans on)")
else:
    print("  (no ghost nodes in this map)")

print("\n=== CLUSTERS (greedy modularity) ===")
for i, c in enumerate(clusters):
    body = ", ".join(x for x in c if not is_nav(x))
    if body: print(f"  C{i} ({len(c)}): {body}")

print("\n=== STRUCTURAL GAPS (cluster pairs with <=1 connecting edge) ===")
pair = defaultdict(int)
for a in adj:
    for b in adj[a]:
        if a < b and cid[a] != cid[b]:
            pair[tuple(sorted((cid[a], cid[b])))] += 1
found = False
for i in range(len(clusters)):
    for j in range(i + 1, len(clusters)):
        if len(clusters[i]) < 2 or len(clusters[j]) < 2: continue
        if pair.get((i, j), 0) <= 1:
            found = True
            ri = [x for x in clusters[i] if not is_nav(x)][:2]
            rj = [x for x in clusters[j] if not is_nav(x)][:2]
            print(f"  C{i} <-> C{j}: {pair.get((i,j),0)} edge  ({', '.join(ri)}... vs {', '.join(rj)}...)")
if not found:
    print("  none: the clusters that exist are bridged. The seam between them")
    print("  (and any ghost sitting on it) is where to look next.")

# ---- reachability ----------------------------------------------------------
comps = connected_components(adj)

print("\n=== REACHABILITY ===")
if len(comps) == 1:
    print(f"  fully connected: all {len(comps[0])} nodes in one component")
else:
    print(f"  {len(comps)} components:")
    for i, c in enumerate(comps):
        if len(c) == 1:
            label = c[0]
            deg = len(adj.get(label, []))
            print(f"  ISLAND (deg {deg}): {label}" + ("   [GHOST]" if is_ghost(label) else ""))
        else:
            print(f"  component {i}: {len(c)} nodes  ({', '.join(c[:3])}{'...' if len(c) > 3 else ''})")

# reachable-but-unlinked: ghost nodes at distance 2 from a non-ghost in the main component
print("\n  reachable-but-unlinked (ghost at distance 2 -- possible missing edge):")
found_ru = False
if comps:
    main = set(comps[0])
    for n in sorted(main):
        if not is_ghost(n): continue
        dist = bfs_all(adj, n)
        for other, d in sorted(dist.items()):
            if d == 2 and other in main and other not in adj[n] and not is_ghost(other):
                print(f"    {n}  --2-->  {other}")
                found_ru = True
if not found_ru:
    print("    none")
