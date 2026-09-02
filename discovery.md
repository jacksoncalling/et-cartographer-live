# Discovery — Pass 1 of the run (inventory and yardstick)

The cartographer runs in **two passes, one session, one folder, one agent**.

- **Pass 1 (this file): Discovery.** The exploratory read. Go wide across everything
  you are handed, from the several angles the lens mix gives you, to understand the
  mental models that shaped the material and what they take for granted. Out of that,
  build the inventory of nouns, mark what is live, pending, leftover, or a
  ghost-candidate, and build the yardstick that later tells you what is missing. It
  ends by writing `Inventory.md`.
- **Pass 2 (`cartography.md`): Cartography.** Wire the nouns, confirm the ghosts,
  hunt the gaps, and write the walkable map.

`Inventory.md` is a checkpoint the same agent hands to itself inside the same run.
Nothing is delivered from one folder or agent to another. This is a system map made
in two disciplined passes, not a pipeline.

Why hold the line between the passes: extraction (what is in the text) and
integration (where it belongs, what moves, what is missing) are different jobs. Fold
them into one prompt and a reader gets cards before the inventory is honest, and a
ghost gets drawn as live because nobody stopped to ask what was actually wired.
Inventory before cards.

## What you are actually mapping

Not "the domain." You are mapping the **mental model a body of work expresses**: the
operative model held by whoever produced these artifacts. Pass 1 finds the shape and
the pieces. Pass 2 finds the relief (see `identity.md`, "Why the map carries relief"):
what shapes the form, and where the holes are.

## What to point it at (source types)

Feed it artifacts, not summaries. Any of:

- **Websites**: landing pages, "about", partner and ecosystem pages, directories.
- **PDFs**: grant applications, reports, research papers, bidbooks, white papers.
- **Markdown and docs**: notes, wikis, READMEs, specs.
- **Code and repos**: source files, module layouts, configs. The mental model of a
  system lives in its structure.
- **Registries and spreadsheets**: member lists, supplier maps, asset inventories.
- **News and newsletters**: transparency over time is itself a signal of how a
  project keeps its ecosystem informed.
- **Events, workshops, education**: listings show how the ecosystem is kept active
  and who is being cultivated.
- **Transcripts**: interviews, talks, meeting notes.

Point the cartographer at these. Do **not** paste them wholesale into the chat. The
cartographer reads sources to build the map. It never copies the source into the
reader's lap.

## The Pass 1 moves

1. **Scope and choose the lens(es).** This step prevents drift. Do four things before
   you gather anything:
   a. **Start from the user.** What did they bring (transcripts, code, PDFs, a
      registry, a vault), and what do they already know they want mapped? Their
      question rules the run. Write it in one line, together with the later reader
      (say if it is a model).
   b. **Classify the territory.** Which track, Technical / Business / Creator, and
      what is its shape and scale? A solo creator's vault is not a cross-border
      megaproject, and the lens must match.
   c. **Assemble a lens mix from `reference/discovery-lenses.md`.** The catalogue is a
      deck. Build a short ordered mix for this territory, one to three lenses, each
      with a role: **open** (expose the shape and the main entities), **deepen** (go
      into the core the opening lens flagged), and optionally **converge** (sharpen
      what the map is really about). A mix of one is valid when the territory is well
      understood. Cap it at three. Write one line of reason per lens. A lens with no
      role and no reason is drift waiting to happen. The mix is the working vocabulary
      you hunt and shelve with in moves 2 and 4.
   d. **Set the external-depth budget.** Decide what, if anything, to research beyond
      the user's material. When the user is explicit about scope, external discovery
      *deepens* the map (analogues, missing pieces, the wider field). It does not
      re-scope the territory. The cartographer adds depth. It does not overrule the
      person who brought the work.
2. **Gather.** Find and pull the artifacts. This includes searching and scraping the
   web for what is out there, not only reading what you were handed. Log every source
   with a link and a date, and to the granularity a card will later cite it at (the
   `path:line`, the `#heading`, the transcript timestamp plus quote), per
   `reference/source-types.md`. A source logged only as a container ("the interview",
   "the repo") will not survive as a citation. (The folder instructs this. The AI
   performs it at run time.)
3. **Build the reference frame (the yardstick).** Before anything can be called a gap,
   build what a complete version of this territory would look like, per
   `reference/reference-frames.md`. Two sources, both cited:
   (a) **ask the user** which models or frameworks they use for this domain; and
   (b) research at least **two comparable analogues**, matched to this territory's
   shape and scale (a corner shop is not measured against CERN). For each analogue, go
   deep: what model they used, what is documented about their successes AND their
   failures, what dimensions they carried. Naming a reference without studying how it
   works and where it broke does not count. The dimensions a complete model should
   carry are read off this evidence, never from your own head or the user's offhand
   remarks. This yardstick is built now, in Pass 1, and spent in Pass 2's gap hunt.
   (For an ET-scale run, two analogues might be Virgo and an ERIC-style multinational
   infrastructure, plus the EU guidance for multi-country collaborations.)
4. **Shelve (the inventory).** Using the working vocabulary of the lens mix, extract
   entities. Give each a **shelf** for the catalog, a grouping drawn from the lens and
   the territory, not a fixed list (the ET run shelved by `governance` / `funding` /
   `engagement`; a Business Model Canvas run by `audience` / `core` / `revenue`). A
   shelf is where a reader finds the card, not a graph edge: edges come only from typed
   movements in Pass 2, so shelving a noun wires it to nothing. A noun that fits no
   shelf sits in `emergent`, or stays unshelved. Do not force it, and do not shelve a
   ghost to make it look connected. Type each against the closed noun set in
   `reference/card-types.md`. Mark each **provisionally**, **from the source alone**:
   live, pending, leftover, or ghost-candidate. This is a source reading, not the final
   verdict: a name with no substance in the text is a ghost-candidate now, and Pass 2
   confirms it once wiring shows whether anything actually connects to it. No cards
   yet. No wiring yet.

## What Pass 1 writes: `Inventory.md`

Write one `Inventory.md` into the run's map folder (for ET that is `map/`; for a new
territory, the folder you create for it). It carries:

- **Run header:** the user's question, the later reader (say if it is a model), the
  territory class, the lens mix with a role and reason per lens, the external-depth
  budget.
- **Source log:** every artifact, with a link and a date, cited to the openable
  locator it will be referenced at (see `reference/source-types.md`).
- **Reference frame:** the analogues studied (model, successes, failures, dimensions)
  and the dimensions a complete version of this territory should carry. This is the
  yardstick Pass 2 measures absence against.
- **Noun inventory:** every entity, with its noun type, its hub, its provisional
  live / pending / leftover / ghost-candidate mark, and its source. Collect the ghost-candidates
  into a list of their own, so Pass 2 knows exactly what to confirm.

`Inventory.md` has no cards and no catalog. It is the honest pile of nouns and the
yardstick. When it is complete, the same agent proceeds to `cartography.md`.

## The discipline (carried from `rules.md`)

- Cite a source for every noun. No source, no noun.
- Mark verified vs open. A ghost-candidate is marked, never invented and never deleted.
- Never fill a silence with a guess. A silence is a research question.
- Do not write cards in this pass. Cards are Pass 2. Inventory before cards.
