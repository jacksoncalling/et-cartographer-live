# Feature Journey: The Living Cartographer (demo for AGIT / Ralf-Peter Meyer)

> Started 2026-09-03. A living artifact of the design conversation. Not a spec yet.

## Context
- The published ET-Cartographer artifact is a **receipt of a cold walk**: walkable but static.
  The reader can look, but cannot feed it, extend it, or be walked through it.
- Audience: technology-transfer managers. There are **four** in the ET Euregio campaign
  (NL, Wallonie/FR-BE, Flanders/NL-BE, Germany/AGIT). First reader: Ralf-Peter Meyer, AGIT.
- Strategic frame: the demo should prove Josh can hand a TT manager a **living instrument for
  the part of the job physicists can't do** — seeing gaps, ghosts, unbridged actors. Not prove
  physics knowledge.
- Deployment pattern (proven on journal-watch-kustos): folder system -> GitHub -> Replit runs
  the frontend.

## Reference experiences
- **InfraNodus** (https://infranodus.com): upload text -> overview -> 3D graph -> zoom to
  detail -> find gaps -> generate ideas. This is the workflow shape Josh admires.
- Josh's own **et-foerder-navigator** (C:\Users\Max Mustermann\et-foerder-navigator): a folder
  system cataloguing grant money for research collaborations. A *future* corpus the cartographer
  could pull from (research phase -> supply-chain phase).

## Struggling Moments
- "Ralf can look at the map but he can't do anything with it."
- "There's no page of sources — no list of what's been uploaded or scanned, and no way to add to it."
- "You can't add to the corpus and make a new pass to update the graph and connections."
- "The map is a single cold walk; it can't be walked *together*, and the dialogue about ghosts
  isn't something a user will just intuitively do."
- (implicit) "It maps one territory for one reader, but four TT managers across four jurisdictions
  could each use it."

## Tension to hold (surfaced early)
- InfraNodus **generates ideas** to fill gaps. The Cartographer's law is **anti-fabrication**:
  never fill a silence with a guess. So the gap dialogue must *interrogate and invite*, not
  auto-generate edges. The soul of the tool is the honest ghost, not the plausible idea.

## Refinement (round 2)
- The agent is **not a rigid pointer**. It is a **bidirectional dialogue partner** that also
  **learns from the user**. Ralf has 30 years of tri-country collaboration knowledge that is
  NOT online. The agent should be able to write that tacit knowledge back into the folder's
  **core learnings** — the same move Josh makes with `/compound`.
- Graph can stay **2-D** (the InfraNodus 3-D globe is not required).
- The agent **initiates**: a hello/welcome message in a chat bar, plus a "click here to get
  started and we'll walk through what's possible" prompt. The walk is offered, not assumed.

## Architecture fork (surfaced, needs a decision)
- Static HTML has no hands. Ingesting sources, re-running passes, and writing back to the
  folder requires a **backend** (Replit runs Node/Python with an Anthropic key + a tool-use
  loop). Capability is not the blocker.
- **The blocker is persistence.** Where do the agent's writes land?
  - Commit back to GitHub (keeps "folder = map = method"; Ralf's edits become commits). [recommended]
  - A database (Supabase; robust, loses the folder elegance).
  - A Replit persistent volume (simplest, siloed).
- Future connection: pull from **et-foerder-navigator** (grant corpus) as a source the agent
  can consult when discussing gaps — a research-phase -> supply-chain-phase bridge.

## DECISION (2026-09-03): Build Option 2 — live dialogue + one real ingest-and-cite loop
- The demo's only job: make Ralf feel *"this sees my ecosystem, and it wants my knowledge."*
- The single moment that carries the whole product: agent walks Ralf to a gap HE recognizes,
  asks about it, and writes his answer back as a **cited card attributed to him**, live.
- Full commit-back-to-GitHub persistence (Option 1) is what the EMAIL promises, not what v1 ships.
- Sequence: (0) rebuild the stale artifact from the current map, (1) wrap in live agent chat +
  welcome + guided walk, (2) wire the single real ingest-and-cite loop.

## Desired Outcomes
1. On landing, Ralf is **greeted and offered a walk** — never dumped into a raw graph. A hello
   in a chat bar + "click here and I'll show you what's possible."
2. Ralf can see the whole territory and **zoom to any object's card**: its type, its
   live/leftover/ghost/pending status, its movements, and its sources.
3. A **Sources page** lists every source in the corpus (uploaded docs + scanned URLs); Ralf can
   **add one** and trigger a fresh pass.
4. The agent can **walk Ralf to a specific gap/ghost** and explain WHY it's marked, without
   fabricating a bridge (interrogative, not generative).
5. When Ralf supplies knowledge, it lands as a **cited card attributed to him**
   (`verified: Ralf-Peter Meyer, interview, 2026-09`) and the map visibly grows.
6. Ralf leaves feeling the map is **his to grow**, not a finished object to admire.

## The governing metaphor: THE SHOP (round 3)
- The map + cards (Josh likes the existing **cards tab**) are the **shop floor**.
- The agent is a **shopkeeper** in a panel on the left or right: greets, then *lets Ralf browse*.
  "Hi, have a look around. When you need help, tell me — I can answer what you're looking at,
  or show you what I found strange."
- **Ralf sets the pace.** He can look, tap, zoom, click cards freely. The shopkeeper is
  *available*, not leading. The guided gap-walk is one thing he can *ask for*, not a rail.
- Escape hatch is the default state, not a special case. This resolves the "30-year expert
  resents being walked" risk.

## The shopkeeper's repertoire (kinds of questions it answers — to confirm/extend)
- "What am I looking at?" (orient to the whole territory)
- "What is this?" (explain a card the user clicked)
- "Where are the gaps / what's missing?" (surface the ghosts)
- "Why aren't these two connected?" (interrogate one gap — never fabricate the bridge)
- "I know something you don't." (ingest + write a cited card attributed to the user)
- "Who should I talk to about X?" (surface actors — the re-contact wedge)
- (maybe) "Show me by country." (filter by the four jurisdictions / four TT managers)
- "What's the newest news?" (refresh a stale/unreachable region from a live feed, e.g.
  https://www.einstein-teleskop.de/news/)

## Voice / identity (round 4)
- The agent must NOT feel like a generic Gemini bolt-on. When invoked, its **system prompt is
  assembled from the folder itself**: identity.md + rules.md + reference/card-types.md +
  reference/source-types.md + the map's Catalog + North Star. It speaks AS the cartographer of
  THIS territory, carrying the anti-fabrication law, the 6 nouns, the status grammar.
- This is a context-assembly job. It is the whole difference between "a chatbot on a website"
  and "the mapmaker who walked this ground."

## Reachability (round 4) — new lens for the gap engine + the agent
- Add to gap-scan.py: **connected components** + **reachability**.
- Reachable-but-unlinked: a path exists via intermediaries, no direct movement recorded.
  Could be a real gap OR an unrecorded edge.
- Unreachable / separate component: an island. Usually means **missing or stale info**, not a
  true void. Triggers a REFRESH move: "this region is old/unreachable, what's the newest news?"
  -> agent offers to ingest from a live feed (ET news) before calling it a gap.

## The gap-bridging dialogue FRAMEWORK (answer: yes, a cheap model NEEDS one)
A Flash-tier model will drift and fabricate without structure. The framework IS the discipline.
And it already exists — it is Josh's own card grammar. The bridging dialogue is a constrained
4-step walk (each step a small, bounded choice the cheap model can make reliably):

1. **CLASSIFY the gap.** Is this a REAL structural gap, or an ARTIFACT of missing/stale info?
   - Use reachability as a prior: unreachable/old region -> lean "missing info", offer refresh.
   - Ask the user to confirm: "Is this genuinely unconnected, or do I just not have the source?"

2. **IDENTIFY the bridge type** (only if confirmed real). What KIND of thing would connect them?
   Walk the 6 nouns as candidate bridges:
   - an **Actor** (a person/org who brokers) — often the answer, and the re-contact wedge
   - a **Shared Resource**, a **Capability**, an **Instrument** (e.g. a funding instrument / MOU),
     a **Decision** not yet made, or a **Jurisdiction** boundary.

3. **STATUS the bridge.** Does it exist?
   - Exists but unrecorded -> user names it -> **cited card, status: live** (attributed to user).
   - In progress -> **status: pending**.
   - Needed but absent -> a real **ghost** -> becomes a research question / "who could build this".

4. **RECORD or QUESTION.** Either write the cited card (bridge exists), or write the ghost + its
   research question (bridge absent). Never invent the bridge itself.

This reuses card-types.md + rules.md verbatim, so the dialogue enforces the method even on a
cheap model. No new framework to invent.

## Journey Map (FINAL — the shop) — approved 2026-09-03
**Trigger:** Ralf opens the link from the email, skeptical, between meetings.

| # | Ralf does | Shop responds | Feel | Outcomes |
|---|---|---|---|---|
| 1 | Lands | Cards/map = the shop floor. Shopkeeper docked far-right (collapsible): "Welcome. Have a look around, tap anything. When you want help, ask — I can tell you what you're looking at, or show you what I found strange." Then waits. | At ease, in control | 1 |
| 2 | Browses — taps cards, zooms, reads | Nothing interrupts. Cards show type, status, sources. | "Real, and mine to poke at" | 2 |
| 3 | Asks a question | Shopkeeper answers THAT question, plain language, pointing at the map. Speaks AS the cartographer (folder-assembled voice). | Helped, not sold to | 2, 4 |
| 4 | Asks / is offered "what's strange?" | Walks him to a **curated gap**. Runs the 4-step bridging walk: classify -> bridge-type (6 nouns) -> status -> record/question. | Recognition | 4 |
| 5 | Tells it what he knows | Restates, asks for the anchor, writes a **cited card in his name**; graph redraws. | Authorship (the aha) | 5, 6 |
| 6 | Opens Sources / adds one | List of the corpus + "add a source" box; one real ingest pass. Reachability may prompt "what's the newest news?" | "It grows when I feed it" | 3 |

### Delight moment
- Step 5: his sentence becoming a cited node with his name on it, graph redrawing.

### Friction risks (held, not solved)
- Curated opening gap must be one Ralf recognizes instantly, or step 4 misfires. **OPEN: pick the gap.**
- Shopkeeper voice must read as in-house expert, not generic model (solved by folder-assembled system prompt).
- Live dialogue must be genuinely live (real LLM), or a 30-year expert breaks the script on contact.

### Open questions to resolve at build time
- Which specific ET-map gap does the walk open on? (pull current top ghosts/gaps and choose)
- Persistence for v1: staged (in-session) writes vs. commit-back-to-GitHub. (Decided: staged for demo; GitHub promised in email.)
- Model: Gemini Flash 2.5 vs Claude Haiku for the shopkeeper. (Framework makes cheap model viable.)

## Build sequence (v1 = Option 2)
0. **Rebuild the stale artifact** from the CURRENT map (graph/card changes postdate the published HTML). Fast, needed regardless, refreshes the link the email points to.
1. **Wrap in the shopkeeper**: docked collapsible chat panel, folder-assembled system prompt, the repertoire, the guided-gap walk. Live LLM (Flash 2.5 or Haiku).
2. **Wire the single real ingest-and-cite loop**: add-a-source box -> discovery on one source -> cited card written -> graph redraws. Staged persistence (in-session) for the demo.
3. Add **reachability** to gap-scan.py (connected components + reachability) so the agent can distinguish real gaps from stale/missing-info islands.
Deploy pattern: folder -> GitHub -> Replit frontend (as with journal-watch-kustos).

## Downstream (not part of this journey, but sequenced after it)
- **Email to Ralf-Peter Meyer (AGIT)**: re-contact wedge, points at the live demo, invites him in
  (promises the GitHub-persistent full version). Draft only; Josh sends.
- **Future**: pull from et-foerder-navigator (grant corpus); the four-TT-manager multi-jurisdiction use.
