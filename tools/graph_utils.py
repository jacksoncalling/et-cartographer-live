# -*- coding: utf-8 -*-
"""Shared graph and parsing primitives for the cartographer tool suite.

Imported by build-artifact.py, build-bundle.py, and gap-scan.py.
"""
import re
from collections import deque, defaultdict

# ---- frontmatter + body parsing ----

def split_fm(txt):
    """Parse YAML frontmatter; return (fm_dict, body). Values preserve case."""
    fm = {}; body = txt
    if txt.startswith("---"):
        end = txt.find("\n---", 3)
        if end != -1:
            for line in txt[3:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip().lower()] = v.strip()
            body = txt[end+4:]
    return fm, body

LINK = re.compile(r"\[\[([^\]|#]+)")

def clean(s):
    """Strip [[wikilink]] bracket syntax, returning plain text."""
    return s.replace("[[", "").replace("]]", "").strip()

def movements_zone(body):
    """Extract typed-movements zone from a post-frontmatter card body.

    Only [[wikilinks]] in this zone count as graph edges. Skips the title
    and description paragraph; stops at Hits / Does-not-hit / Source lines.
    """
    lines = body.splitlines()
    past_title = False; past_desc = False; zone = []
    for line in lines:
        s = line.strip()
        if not past_title:
            if s.startswith("# "): past_title = True
            continue
        if not past_desc:
            if not s: past_desc = True
            continue
        sl = s.lower()
        if sl.startswith("- hits:") or sl.startswith("- does not hit:"): break
        if sl.startswith("source:"): break
        if s: zone.append(line)
    return "\n".join(zone)

def parse_body(body):
    """Parse a card body; return (title, desc, hits, miss, source).

    Strips [[wikilink]] brackets from desc, hits, and miss so consumers
    receive plain text. Source is kept verbatim (contains URLs and path:line).
    """
    lines = body.splitlines()
    title = None; i = 0
    for idx, l in enumerate(lines):
        if l.startswith("# "): title = l[2:].strip(); i = idx+1; break
    while i < len(lines) and not lines[i].strip(): i += 1
    desc = []
    while i < len(lines) and lines[i].strip():
        desc.append(lines[i].strip()); i += 1
    hits = miss = source = None
    for idx, l in enumerate(lines):
        s = l.strip()
        if s.lower().startswith("- hits:"):
            hits = clean(s.split(":", 1)[1].strip())
        elif s.lower().startswith("- does not hit:"):
            miss = clean(s.split(":", 1)[1].strip())
        elif s.lower().startswith("source:"):
            parts = [s.split(":", 1)[1].strip()]
            j = idx + 1
            while j < len(lines) and lines[j].strip():
                parts.append(lines[j].strip()); j += 1
            source = " ".join(p for p in parts if p)
    return title, clean(" ".join(desc)), hits, miss, source

# ---- graph algorithms ----

def brandes(adj):
    """Brandes betweenness centrality (undirected; divide-by-2 applied)."""
    CB = {v: 0.0 for v in adj}
    for s in adj:
        S=[]; P={w:[] for w in adj}; sig={w:0 for w in adj}; sig[s]=1
        d={w:-1 for w in adj}; d[s]=0; Q=deque([s])
        while Q:
            v=Q.popleft(); S.append(v)
            for w in adj[v]:
                if d[w]<0: d[w]=d[v]+1; Q.append(w)
                if d[w]==d[v]+1: sig[w]+=sig[v]; P[w].append(v)
        dl={w:0.0 for w in adj}
        while S:
            w=S.pop()
            for v in P[w]: dl[v]+=(sig[v]/sig[w])*(1+dl[w])
            if w!=s: CB[w]+=dl[w]
    for v in CB: CB[v]/=2.0
    return CB

def communities(adj):
    """Greedy modularity community detection. Returns {node: community_label}."""
    m = sum(len(v) for v in adj) // 2
    if m == 0: return {n: i for i, n in enumerate(adj)}
    cof = {n: n for n in adj}; members = {n: {n} for n in adj}
    degc = {n: len(adj[n]) for n in adj}
    def lij(a, b):
        return sum(1 for x in members[a] for y in adj[x] if cof[y] == b)
    improved = True
    while improved:
        improved = False; best = None; bestdq = 1e-9
        pairs = set()
        for x in adj:
            for y in adj[x]:
                a, b = cof[x], cof[y]
                if a != b: pairs.add(tuple(sorted((a, b))))
        for (a, b) in pairs:
            dq = lij(a, b) / m - (degc[a] * degc[b]) / (2 * m * m)
            if dq > bestdq: bestdq = dq; best = (a, b)
        if best:
            a, b = best; members[a] |= members[b]
            for n in members[b]: cof[n] = a
            degc[a] += degc[b]; del members[b]; del degc[b]; improved = True
    return cof

def connected_components(adj):
    """Return list of components (sorted lists of node ids), largest first."""
    visited = set(); comps = []
    for start in sorted(adj):
        if start in visited: continue
        comp = []; q = deque([start]); visited.add(start)
        while q:
            v = q.popleft(); comp.append(v)
            for w in adj[v]:
                if w not in visited: visited.add(w); q.append(w)
        comps.append(sorted(comp))
    return sorted(comps, key=lambda c: -len(c))

def bfs_all(adj, start):
    """Return {node: distance} for all nodes reachable from start via BFS."""
    dist = {start: 0}; q = deque([start])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist: dist[w] = dist[v] + 1; q.append(w)
    return dist
