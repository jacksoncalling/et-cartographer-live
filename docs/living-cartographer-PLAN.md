# Feature Implementation Plan: The Living Cartographer (shopkeeper demo)

**Overall Progress:** `0%`

> Handoff note for the building model: read
> [.claude/feature-journeys/living-cartographer-demo.md](.claude/feature-journeys/living-cartographer-demo.md)
> FIRST — it is the full design rationale (the shop metaphor, the anti-fabrication law, the
> 4-step bridging framework). Then read the project `CLAUDE.md`. This plan is the build order;
> that doc is the why. Do not add scope beyond what is listed here.

## TLDR
Turn the static ET-Cartographer artifact into a **living demo** for a technology-transfer
manager (Ralf-Peter Meyer, AGIT). The map/cards stay the "shop floor"; a **shopkeeper agent**
docks to the side, greets, waits, and — when asked — answers questions, walks the user to a
curated gap, and writes the user's own tacit knowledge back into the map as a **cited card in
their name**, redrawing the graph. Deploy folder -> GitHub -> Replit, matching journal-watch-kustos.
This is **Option 2**: live dialogue + one real ingest-and-cite loop, **staged (in-session)
persistence**. Full commit-back-to-GitHub is promised in the email, not built here.

## Critical Decisions
- **Metaphor = the shop.** Agent is available, not leading. Escape hatch (free browsing) is the
  default state. Docked collapsible chat panel as a third column; never covers the cards.
- **Agent voice = folder-assembled.** System prompt is built from `identity.md` + `rules.md` +
  `reference/card-types.md` + `reference/source-types.md` + the map's `Catalog` + `North Star`.
  It speaks AS the cartographer of THIS territory, not a generic chatbot.
- **Anti-fabrication stays law.** The agent never invents a bridge. User knowledge is recorded
  as a CITED source (`verified: <name>, interview, <date>`), never as a guess. This is what lets
  "the agent learns from the user" coexist with "the agent never fabricates".
- **Cheap model + framework, not a smart model freelancing.** Target Gemini Flash 2.5 or Claude
  Haiku. The 4-step bridging framework (classify -> bridge-type via the 6 nouns -> status ->
  record/question) is what holds the discipline on a cheap model. Framework already exists as the
  card grammar; do not invent a new one.
- **Reachability** distinguishes a real gap from a stale-info island; a disconnected component
  triggers a "what's the newest news?" refresh offer, not a gap label.
- **Shared data contract.** Frontend and agent backend both consume ONE `map.json` bundle emitted
  from the map folder, so there is a single source of truth.
- **Reuse, don't rewrite.** `tools/build-artifact.py` + `tools/template.html` already render the
  cards/network from a `DATA` blob. Extend that template; do not build a new frontend from scratch.

## Tasks:

> **Ownership:** Steps 0-3 and 9 are **CLI** (deterministic Python + Josh's decisions; commit
> `map.json` before the app starts). Steps 4-8 are the **Replit app** (consumes `map.json`, never
> re-derives the graph). Do the CLI steps first.

- [ ] 🟥 **Step 0 (CLI): Refresh the published ET artifact (stale — predates graph/card changes)**
  - [ ] 🟥 Run `python tools/build-artifact.py map` -> writes `output/et-cartographer.html`
  - [ ] 🟥 Preview via `python -m http.server 8137` at `/output/et-cartographer.html`; sanity-check node/edge counts + hero ghost line in stdout
  - [ ] 🟥 Republish `output/et-cartographer.html` to the SAME artifact URL (same file path) so the email's link is current

- [ ] 🟥 **Step 1 (CLI): Add reachability to `tools/gap-scan.py`**
  - [ ] 🟥 Compute connected components on the existing object `adj` graph (BFS over the same nav-excluded graph)
  - [ ] 🟥 Report: multi-node components as "islands"; flag pairs that are reachable-but-unlinked (path exists via intermediaries, no direct edge)
  - [ ] 🟥 Keep the change consistent with `build-artifact.py`'s graph rule (same `movements_zone`, same nav exclusion) — do not diverge the two graphs

- [ ] 🟥 **Step 2 (CLI): Emit a shared `map.json` bundle (single source of truth)**
  - [ ] 🟥 New tool `tools/build-bundle.py <map-folder>` (or extend `build-artifact.py`) that writes `<map-folder>/map.json`
  - [ ] 🟥 Bundle contents: the existing `DATA` (nodes/edges/hero/topReal/northStar) PLUS per-card full description, movements, sources, and the reachability/component data from Step 1
  - [ ] 🟥 Reuse the exact parsing from `build-artifact.py` (`split_fm`, `parse_body`, `movements_zone`) so the bundle graph == the artifact graph

- [ ] 🟥 **Step 3 (CLI + Josh): Pick the curated opening gap (make step-4 of the journey land)**
  - [ ] 🟥 Run `python tools/gap-scan.py map` and read REAL HUBS, LOAD-BEARING ABSENCE, STRUCTURAL GAPS
  - [ ] 🟥 With Josh, choose ONE gap/ghost Ralf will recognize instantly (favor an Actor-brokered, tri-country gap)
  - [ ] 🟥 Record the chosen gap id + the opening question in `map/build.json` under a new `demo.openingGap` key (agent reads it)

- [ ] 🟥 **Step 4 (Replit): Frontend — dock the shopkeeper panel into `tools/template.html`**
  - [ ] 🟥 Add a collapsible right-hand chat column; cards/network stay the primary surface, never covered
  - [ ] 🟥 Welcome message on load (shop greeting, then waits — no auto-walk)
  - [ ] 🟥 Chat input posts to the backend `/chat` endpoint; render streamed replies
  - [ ] 🟥 On an ingest result, redraw the graph with the new node + edge (reuse the existing force-layout render path)
  - [ ] 🟥 Keep the ET header edit-points (title/subtitle/footer) intact; this template still serves the ET territory

- [ ] 🟥 **Step 5 (Replit): Backend — the shopkeeper agent (Node or Python)**
  - [ ] 🟥 Server with an LLM client (Gemini Flash 2.5 or Claude Haiku; key in Replit secrets)
  - [ ] 🟥 Assemble the system prompt at startup from `identity.md` + `rules.md` + `reference/card-types.md` + `reference/source-types.md` + `map/Catalog.md` + `map/North Star.md`
  - [ ] 🟥 Load `map.json` as the agent's ground truth; expose the map + reachability as retrievable context
  - [ ] 🟥 `/chat` endpoint: message in, cartographer reply out (streamed)

- [ ] 🟥 **Step 6 (Replit): Wire the repertoire + the 4-step bridging framework**
  - [ ] 🟥 Repertoire intents: orient, explain-a-card, surface-gaps, interrogate-one-gap, who-should-I-talk-to, (optional) filter-by-country, what's-the-newest-news
  - [ ] 🟥 Bridging framework as an explicit state machine in the prompt/code: (1) classify real-vs-missing-info (use reachability prior) (2) identify bridge-type from the 6 nouns (3) status the bridge (live-unrecorded / pending / ghost) (4) record-or-question
  - [ ] 🟥 Guard rail in code: the agent may NEVER emit an edge/card without a source; absent bridge -> ghost + research question, never an invented link

- [ ] 🟥 **Step 7 (Replit): The single ingest-and-cite loop (staged persistence)**
  - [ ] 🟥 "Add a source" box + a Sources view listing the corpus from `map.json`
  - [ ] 🟥 On user knowledge or a pasted source: run the bridging framework; build a new card object with `source: verified: <name>, interview, <date>`
  - [ ] 🟥 Write to an IN-SESSION copy of the map (not GitHub); return the new node/edge to the frontend to redraw
  - [ ] 🟥 (Optional, if a source URL is given) run a light discovery pass on that one source and show the card(s) it would add

- [ ] 🟥 **Step 8 (Replit): Deploy (folder -> GitHub -> Replit)**
  - [ ] 🟥 Push the repo; import into Replit; set LLM key + any config in Replit secrets
  - [ ] 🟥 Confirm the shop loads, the shopkeeper speaks in-character, the curated gap walk runs, and the ingest loop redraws the graph live
  - [ ] 🟥 Capture the public Replit URL for the email

- [ ] 🟥 **Step 9 (CLI, promise not build): note the GitHub-commit persistence path**
  - [ ] 🟥 Leave a short `FUTURE.md` describing the Option-1 upgrade (agent writes -> GitHub commit) so the email's promise is backed by a written path, and the et-foerder-navigator corpus connection
