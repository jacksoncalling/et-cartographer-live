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
from collections import deque, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
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

def split_fm(txt):
    fm = {}
    body = txt
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
def clean(s): return s.replace("[[", "").replace("]]", "").strip()

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

def parse_body(body):
    lines = body.splitlines()
    title = None; i = 0
    for idx, l in enumerate(lines):
        if l.startswith("# "): title = l[2:].strip(); i = idx+1; break
    while i < len(lines) and not lines[i].strip(): i += 1
    desc = []
    while i < len(lines) and lines[i].strip():
        desc.append(lines[i].strip()); i += 1
    hits = miss = None
    source = None
    for idx, l in enumerate(lines):
        s = l.strip()
        if s.lower().startswith("- hits:"): hits = clean(s.split(":", 1)[1])
        elif s.lower().startswith("- does not hit:"): miss = clean(s.split(":", 1)[1])
        elif s.lower().startswith("source:"):
            # capture the Source line plus any following non-blank lines (the
            # optional multi-line [S#] tag form), so the whole reference list is kept.
            parts = [s.split(":", 1)[1].strip()]
            j = idx + 1
            while j < len(lines) and lines[j].strip():
                parts.append(lines[j].strip()); j += 1
            source = " ".join(p for p in parts if p)
    return title, clean(" ".join(desc)), hits, miss, source

def movements_zone(body):
    """Extract the typed-movements zone where [[wikilinks]] count as edges.
    Skips title + description paragraph; stops at Hits/Does-not-hit/Source."""
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

def brandes(adj):
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
    m=sum(len(v) for v in adj)//2
    if m==0: return {n:0 for n in adj}
    cof={n:n for n in adj}; members={n:{n} for n in adj}; degc={n:len(adj[n]) for n in adj}
    def lij(a,b): return sum(1 for x in members[a] for y in adj[x] if cof[y]==b)
    improved=True
    while improved:
        improved=False; best=None; bestdq=1e-9
        pairs=set()
        for x in adj:
            for y in adj[x]:
                a,b=cof[x],cof[y]
                if a!=b: pairs.add(tuple(sorted((a,b))))
        for (a,b) in pairs:
            dq=lij(a,b)/m-(degc[a]*degc[b])/(2*m*m)
            if dq>bestdq: bestdq=dq; best=(a,b)
        if best:
            a,b=best; members[a]|=members[b]
            for n in members[b]: cof[n]=a
            degc[a]+=degc[b]; del members[b]; del degc[b]; improved=True
    return cof

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
# "how much of the map moves if this one changes", so a cold reader never meets a
# raw betweenness figure. The number is kept for the card's hover tooltip.
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
            northStar=north_star)

tpl = read(TEMPLATE)
html = tpl.replace("/*__DATA__*/", "const DATA = " + json.dumps(DATA, ensure_ascii=False) + ";")
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", os.path.abspath(OUT))
print("nodes", len(nodes), "edges", len(edges), "clusters", len(ranked))
print("hero ghost:", hero_id, round(hero_bet, 1), "| top real:", top_id, round(top_bet, 1))
print("shelves used:", sorted(set(n["shelf"] for n in nodes)))
