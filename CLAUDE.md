# ET-Cartographer Live — Project Context

> For Claude: load this at the start of every session.
> For Replit operators: this is the architectural map of the codebase.

---

## What This Is

A **living cartographic demo** built for technology-transfer managers in the Einstein
Telescope Euregio campaign. The map shows 41 objects — actors, instruments, funding
vehicles, decisions, and 6 named gaps — across the DE/BE/NL Euregio. A docked
**shopkeeper agent** answers questions, walks the user to a curated gap, and can write
what the user knows back into the map as a cited card, redrawing the graph.

First reader: Ralf-Peter Meyer, AGIT (Aachen tech transfer).

Design rationale and build plan: `docs/living-cartographer-demo.md` and
`docs/living-cartographer-PLAN.md`.

---

## Current State — Updated 2026-09-03

### What's working
- **GitHub:** https://github.com/jacksoncalling/et-cartographer-live
- **Replit:** deploy via `npm start` — Express serves the artifact + `/chat` SSE endpoint
- **Map:** 41 objects, 63 edges, 2 components. Hero ghost: Financing vehicle (83.8 bet).
  Top real hub: ET-InnoNet (218.9 bet).
- **Shopkeeper:** Claude Haiku 4.5, streamed via SSE. System prompt assembled from the
  cartographer folder files + map summary. Anti-fabrication law enforced.
- **Ingest loop:** shopkeeper can propose a new card mid-conversation; frontend adds it
  to the live graph without a page reload. In-session only (not committed to GitHub yet).
- **Sources panel:** left rail lists every cited source from the map cards; user can
  paste a new source and send it to the shopkeeper.
- **graph_utils.py:** shared module for all Python tools — no more duplicate copies of
  `brandes`, `split_fm`, `movements_zone`, etc.

### Known issues / next steps
- **Ingest persistence:** new cards live only for the session tab. GitHub commit-back
  (GitHub Contents API) is the promised upgrade. See `FUTURE.md`.
- **map/map.json must be rebuilt** after any card edit:
  `python tools/build-bundle.py map` then `python tools/build-artifact.py map`.
- **Opening gap** is set in `map/build.json` under `"demo": {"openingGap": "..."}`.
  Currently: `Value capture (ghost)`.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Cartographer method | Markdown folder (`identity.md`, `rules.md`, `reference/`) read by the agent |
| Map source | `map/objects/*.md` — one note per object, `[[wikilinks]]` for edges, YAML frontmatter |
| Bundle | `map/map.json` — emitted by `tools/build-bundle.py`; nodes carry betweenness tier, component, clean text |
| Artifact | `output/et-cartographer.html` — self-contained HTML emitted by `tools/build-artifact.py` |
| Backend | `server.js` — Node/Express; serves the artifact + streams Anthropic API via SSE at `/chat` |
| Shopkeeper model | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`); override via `MODEL_ID` env var |
| Deploy | Replit — `.replit` sets `npm start`, port 3000 maps to external 80 |

---

## Architecture

```
map/objects/*.md  (the cards)
       |
       v
tools/build-bundle.py  --> map/map.json  (data contract)
tools/build-artifact.py  --> output/et-cartographer.html  (the static artifact)
       |
       v
server.js
  GET /       serves output/et-cartographer.html
  POST /chat  reads map/map.json + cartographer folder -> builds system prompt
              streams Anthropic API -> SSE text + ingest events -> browser
       |
       v
tools/template.html  (embedded in et-cartographer.html)
  - catalog panel (left)
  - card + graph view (center)
  - shopkeeper chat panel (right, docked)
  - sources panel (toggle)
```

**The folder IS the agent's operating instructions.** Each file does one job:

- `identity.md` — who the cartographer is, the territory, the reader
- `rules.md` — anti-fabrication law, live/pending/leftover/ghost marking, gap types, refusals
- `discovery.md` — Pass 1 protocol (inventory + reference frame)
- `cartography.md` — Pass 2 protocol (wiring, ghost confirmation, gap hunting, card writing)
- `examples.md` — worked card examples; included in agent context so it knows the schema
- `reference/card-types.md` — the 6 nouns, canonical movements, walk order
- `reference/source-types.md` — citation grammar; `path:line` locators become clickable links
- `reference/gap-heuristics.md` — by-hand gap scan + how to read the computed report
- `reference/reference-frames.md` — how to build the absence yardstick per run (never canned)
- `reference/discovery-lenses.md` — reading models for classifying a territory
- `reference/glossary.md` — lookup surface for every term

---

## Object-note schema (`map/objects/*.md`)

```
---
type: Actor | Capability | Shared Resource | Instrument | Decision | Jurisdiction | Ghost | Tension | Gradient
status: live | leftover | ghost | pending
kind: <optional, e.g. "national research funder">
hub: <optional, e.g. "engagement">
---
# Label

One prose paragraph. Links to neighbours as [[wikilinks]].

Typed movements as prose: Holds [[X]] · funded-by [[Y]] ...

- Hits: what moves if this changes.
- Does not hit: the obvious wrong neighbour.

Source: <URL or path:line — the build renders this as a clickable link>
```

Graph: nodes = object notes; edges = resolved `[[wikilinks]]` in the movements zone only.
Nav nodes (`Catalog`, `North Star`) are excluded from the graph in all tools.

---

## Key File Paths

| What | Where |
|---|---|
| Cartographer method | `identity.md`, `rules.md`, `discovery.md`, `cartography.md`, `examples.md` |
| Reference | `reference/` (6 files — card-types, source-types, gap-heuristics, reference-frames, discovery-lenses, glossary) |
| ET Euregio map source | `map/Catalog.md`, `map/North Star.md`, `map/objects/*.md` |
| Map data bundle | `map/map.json` (rebuilt by `build-bundle.py` — never hand-edit) |
| Build config | `map/build.json` (template, output name, shelf rules, repo_base, openingGap) |
| Gap report | `tools/gap-scan.py` |
| Bundle builder | `tools/build-bundle.py` |
| Artifact builder | `tools/build-artifact.py` |
| Shared graph primitives | `tools/graph_utils.py` (split_fm, clean, movements_zone, parse_body, brandes, communities, connected_components, bfs_all) |
| Artifact template | `tools/template.html` |
| Backend | `server.js` |
| Generated artifact | `output/et-cartographer.html` (do not hand-edit) |
| Design docs | `docs/living-cartographer-demo.md`, `docs/living-cartographer-PLAN.md` |

---

## How to run

```bash
# rebuild the bundle (required after any card edit)
python tools/build-bundle.py map

# rebuild the artifact HTML
python tools/build-artifact.py map

# run the gap report
python tools/gap-scan.py

# start the shopkeeper server locally (needs ANTHROPIC_API_KEY in env)
npm install
npm start
# -> http://localhost:3000
```

**Replit:** set `ANTHROPIC_API_KEY` as a secret, click Run. The `.replit` file handles everything.

---

## Patterns and Gotchas

- **Rebuild both after card edits.** `build-bundle.py` emits the data the server reads;
  `build-artifact.py` emits the HTML the server serves. Both must be in sync.
- **Nav nodes are excluded from the graph.** `Catalog` links to everything; including it
  distorts every betweenness score. All tools drop `type: meta` nodes before computing.
- **Two ghost flavors.** Named-but-unwired (no real edges) and required-but-absent
  (link the chain needs, appears nowhere). Both marked, never deleted.
- **Ingest nodes need `cluster`, not `component`.** `build-artifact.py` uses `cluster`
  (0 or 1 for the two community halves); `build-bundle.py` uses `component` (connected-
  component index). `ingestNode()` in the template translates `component` to `cluster`
  before pushing to the graph.
- **The reference frame is earned, never canned.** Build it per run from the user's
  named frameworks + two deeply-researched analogues. A dimension with no source is a
  bias; drop it.
- **Do not hand-edit `output/et-cartographer.html`.** Change `map/` notes or
  `tools/template.html`, then rerun the builders.
- **`graph_utils.py` is the single source** for `split_fm`, `brandes`, and friends.
  Do not copy these functions into other files.

---

## Workflow Rules (for Claude sessions)

- Start every session by reading this file and noting the Current State date.
- The map is the output; the folder is the method. To change the map, edit `map/` and rebuild.
- Cite source for every card; mark verified vs open; never fill a silence with a guess.
- Keep `gap-scan.py` and `build-artifact.py` consistent on graph-construction rules.
- Do not commit or push without Josh asking.
- No em-dashes in anything user-facing. Ever.
