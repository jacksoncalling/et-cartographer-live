# ET-Cartographer Live

A living map of the Einstein Telescope Euregio campaign — 41 objects, 6 named gaps, and
a shopkeeper agent you can talk to.

**Walk the map:** https://claude.ai/code/artifact/a1e73ced-ee6b-4fb0-afd5-4905e4061bce

---

## What this is

The Einstein Telescope is a proposed gravitational-wave observatory. Nine countries are
competing to host it. The Euregio Meuse-Rhine — the tri-border region of Germany,
Belgium, and the Netherlands — is the European candidate. AGIT, KU Leuven, ULiege, and
a consortium of national funders are running the campaign.

This repo maps that campaign as a graph. Not a list of names, but a network: who holds
what, what moves if you touch one thing, and what the campaign references but has not yet
built. The sharpest finding is a load-bearing absence: a cross-border financing vehicle
that every funding body points toward and that does not yet exist.

The map is built with **The Cartographer** — a method that turns a body of public sources
into a typed graph of actors, capabilities, instruments, decisions, jurisdictions, and
ghosts (named gaps). Each object gets one card, cited to a source. The gaps are named and
kept, never deleted.

The living demo adds a **shopkeeper agent**: a docked chat panel that answers questions,
walks you to the curated gap, and can write what you know back into the map as a cited
card in your name, redrawing the graph.

---

## The map at a glance

| | |
|---|---|
| Territory | Einstein Telescope Euregio campaign (DE / BE / NL) |
| Objects | 41 (35 live, 6 named gaps) |
| Edges | 63 typed movements |
| Top real hub | ET-InnoNet (crosses the most paths) |
| Load-bearing absence | Cross-border financing vehicle (references it; no one has built it) |
| Opening gap for Ralf | Value capture — who captures value if the ET is hosted here |

---

## How to run

**On Replit (the live demo):**

1. Import this repo into Replit.
2. Set `ANTHROPIC_API_KEY` as a secret.
3. Click Run. It starts `npm start` — the server is at port 3000.

**Locally:**

```bash
npm install
ANTHROPIC_API_KEY=sk-... npm start
# -> http://localhost:3000
```

**Rebuild the map after editing cards:**

```bash
python tools/build-bundle.py map      # regenerates map/map.json
python tools/build-artifact.py map    # regenerates output/et-cartographer.html
```

---

## How the app works

```
map/objects/*.md  (the 41 cards, cited to sources)
       |
       v
tools/build-bundle.py  -->  map/map.json       (data contract)
tools/build-artifact.py  -->  output/et-cartographer.html
       |
       v
server.js  (Express)
  GET /       serves the artifact
  POST /chat  reads the cartographer folder + map summary
              streams Claude Haiku 4.5 via SSE
              emits typed ingest events when the agent proposes a new card
```

The chat panel is a third column docked to the artifact. The agent speaks as the
cartographer of this territory — assembled from `identity.md`, `rules.md`, the reference
files, and a compact map summary. It never invents. If it does not know, it says so and
marks the gap as open.

The **ingest loop**: when a user shares knowledge the map does not yet hold, the agent
emits a structured card at the end of its response. The frontend parses it, adds the node
to the live graph, and redraws — no page reload. The card is attributed to the person who
shared it. In-session only; GitHub commit-back is the next step (`FUTURE.md`).

---

## The cartographer method

The map was built in two passes following the folder's instructions:

**Pass 1 (`discovery.md`):** read the public corpus, classify the territory, build a
reference frame from two deeply-researched analogues. Write `map/Inventory.md`.

**Pass 2 (`cartography.md`):** wire the nouns, confirm ghosts by the degree tripwire,
hunt gaps (internal structural + external reference-frame), write catalog and cards,
each citing its source.

`examples.md` shows the schema in miniature.

### THE ONE RULE (for a cold model reading this map)

> **Load the catalog, then one card, then stop. Never load the whole objects folder.**

Ask one question. The catalog points you to one card in two hops. Open that card. Then
stop. Loading everything defeats the point: the catalog exists so you do not have to.

### What the cartographer will refuse

- To hand you the whole source (that is a photocopy, not a map).
- To list everything (that is an auditor).
- To explain why something failed (that is a diagnostician).
- To fill a silence with a guess (that is fabrication).

---

## File map

| Path | What it does |
|---|---|
| `identity.md` | Who the cartographer is, what territory it walked, who the reader is |
| `rules.md` | Anti-fabrication law, status marking, gap types, refusals |
| `discovery.md` | Pass 1 protocol: inventory and reference frame |
| `cartography.md` | Pass 2 protocol: wiring, ghost confirmation, gap hunting, card writing |
| `examples.md` | Schema in miniature — agent reads this to know the card format |
| `reference/` | card-types, source-types, gap-heuristics, reference-frames, discovery-lenses, glossary |
| `map/objects/*.md` | The 41 object cards |
| `map/map.json` | Computed bundle: betweenness tiers, components, hero ghost, top real hub |
| `map/build.json` | Build config: template, output name, shelf rules, opening gap for the demo |
| `server.js` | Express backend: serves artifact + streams `/chat` SSE endpoint |
| `tools/build-bundle.py` | Emits `map/map.json` from the card files |
| `tools/build-artifact.py` | Renders the walkable HTML artifact |
| `tools/gap-scan.py` | Gap report: betweenness, clusters, structural gaps, reachability |
| `tools/graph_utils.py` | Shared graph primitives (split_fm, brandes, communities, etc.) |
| `tools/template.html` | Artifact template: catalog + card + graph + shopkeeper panel |
| `output/et-cartographer.html` | The built artifact (do not hand-edit; rebuild from map/) |
| `FUTURE.md` | Upgrade path: GitHub-persistent card writes, corpus integration |
| `docs/` | Design rationale and build plan for the living demo |

---

## Built on

- **ICM (Interpretable Context Methodology)**, Van Clief and McDermott. Folder as
  architecture, catalog-then-card discipline, walk test.
  [Paper](https://arxiv.org/abs/2603.16021) and [Clief Notes](https://www.skool.com/cliefnotes).
- **Simone Cicero (Boundaryless).** Ecosystem-mapping vocabulary: entities, the VRIO
  liveness test for a capability, the Platform Design Toolkit lens.
- **Bonnitta Roy.** Evaluative AI and topology mapping: reading tensions and contact
  pressure in a field that a map of entities alone cannot show.
- **Michel Bauwens.** Commons and federation vocabulary for naming governance gaps.
- **InfraNodus** (Dmitry Paranyushkin). The north-star behaviour: surface the structural
  gap, do not tour the text.
- **Terroir.** The evaluative layer (tensions, gradients) and the rule that the structure
  detects while the model only voices, and never invents. (Joshua Baker)
