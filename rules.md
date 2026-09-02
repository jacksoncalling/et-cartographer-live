# Rules — how the cartographer maps

> This file governs the *act* of mapping. The card grammar (the 6 nouns, the
> movements, the walk order, the naming collisions) lives in `reference/card-types.md`.
> This file says how to decide, how to mark, and how to refuse.

---

## THE LAW — anti-fabrication (not negotiable)

Ported from the DAS GESETZ of the ET-Förder-Navigator. A cold reader, human or
model, will act on this map. One invented object and the map is worse than nothing.

1. **Every card cites its source.** A link, a file, a dated document. No source, no
   card. A claim with no anchor does not get written down as a fact. The citation
   names the **smallest openable locator**, not the container: a `path:line`, a
   `#heading`, a page, or a transcript timestamp plus a short verbatim quote, never
   just "the repo" or "the interview". The full grammar (the two source kinds, the
   granularity rule, the optional inline tags and `verified:` stamp) is
   `reference/source-types.md`. The one test: a reader must reach the exact passage
   in one hop.
2. **Verified vs open is always marked.** live / pending / leftover / ghost is visible
   on every object (below). A pending or ghost object never renders as live fact.
3. **The model voices; the structure detects.** The cartographer names what the
   sources contain and where they are silent. It never fills a silence with an
   invented object. (An agent once fabricated a whole interview because a name in
   its graph had no wiring. That is the failure this law exists to prevent.)
4. **The map is a prototype pointing at the territory, never the territory.** If a
   card and the real file disagree, the file wins and the card is wrong. Fix the
   card; log it (see the Correction Log in `examples.md`).

---

## WHAT COUNTS AS A NOUN (a card)

An object earns a card only if it is exactly one of the six types in
`reference/card-types.md` **and** it is named in a source. If a candidate is:

- a *relationship* between two objects → it is a **movement**, not a card.
- a *directional pressure with a cost and a threshold* → it is a **gradient**.
- a *structural conflict, both sides live* → it is a **tension**.
- a *value or aspiration with no holder, instrument, or source* → it is a **ghost**
  (mark it, do not delete it), or it is not on the map at all.

Do not promote a wish to a noun. Mapping a wish as live is how the next reader
builds the wrong world.

---

## MARKING — live / pending / leftover / ghost

The single most important act. It is **mechanical**, not a judgment call:

- **Live** — named in a current source **and** wired: it has a holder, an
  instrument, an authority, or money actually routing. (green)
- **Pending** — named in a source as forthcoming or in preparation, not yet wired,
  but on a credible, sourced path to becoming live (a bidbook in preparation; a
  decision on a set track but not yet made). Not a ghost, which has no sourced path;
  not a leftover, which was once live. (pending)
- **Leftover** — was live, still referenced, no longer load-bearing. Honest
  residue. Mark it so no one treats it as current. (amber)
- **Ghost** — **named but unwired.** Referenced in the body of work, but no source
  gives it a holder, an instrument, an authority, or a money path. A ghost is a
  tripwire, not a lie. (unwired)

**Capability liveness — the VRIO check** (from Cicero / Boundaryless). A capability
is live only if it passes **Organized**: someone actually holds and can exercise it.
A capability that is Valuable-Rare-Inimitable but held by no one is a **ghost
capability**. "Everyone says the region can do X" is not the same as "an actor holds
X." Name the holder or mark the ghost.

---

## THE TWO GAPS (this is the product)

The map's value is not the cards. It is what the cards make visible. Two gap types,
both found by walking the catalog, neither needing graph math (the cheap version of
InfraNodus's structural-hole detection):

1. **Ghost** — a *node* present by name, absent in wiring (see marking above).
2. **Structural gap** — two *live* clusters with **no movement between them**. Both
   sides are real; the connecting edge is missing. (Example: the live
   research-capability cluster and the live governance cluster, with no financing
   instrument bridging them — the "excellent nodes, missing mycelium" gap.)

Surfacing a gap is never a recommendation. The map says "these two are not linked"
or "this name has no wiring." It does not say "you should link them" or "here is the
law you are missing." Naming the gap is the job; prescribing the fix is a different
job (a diagnostician's), and out of scope.

---

## RESEARCH, DON'T ASSUME (the seam to a coordination layer)

The cartographer takes nothing at face value. A source is evidence, not truth.

- When a critical object is **absent** (no one names who leads it, no document shows
  the tax treatment, no source routes the financing), that absence is itself a
  finding. Do not shrug and do not guess. Emit a **research question** and mark the
  object `UNVERIFIED — research: <question>`.
- The map's sharp edge is the honest list of what must be researched: "How do other
  multi-country research infrastructures govern cross-border financing?" "Who
  actually leads the tax question, and is it transparent?" These are outputs, not
  failures.
- **Two tiers.** (a) With no tools, the cartographer marks UNVERIFIED + the
  question, and stops. It never fabricates the answer. (b) With research tools, it
  *goes and looks*, cites what it finds, and upgrades the object to live / leftover
  / ghost with a source. A coordination layer is just tier (b) running continuously
  over the whole map.

This is what keeps the map honest and what lets it grow into something that
coordinates, not just describes.

## MOVEMENTS — how nouns link (more than a wiki)

Every card carries its **typed backlinks** (holds, governs, routes-funds-to,
depends-on, decides, contested-by). Links are how a reader hops from one card to the
next in two steps. A wiki links by hyperlink; this map links by *typed relationship
plus consequence*, which is why every card ends with Hits / Does not hit.

---

## HITS / DOES NOT HIT — required on every card

- **Hits** — the objects that move if you change this one. Follow the backlinks.
- **Does not hit** — the obvious wrong neighbour: the word everyone reaches for that
  this change does *not* touch. Without this line, a card is a glossary entry, not a
  map. Always name the wrong neighbour explicitly.

---

## REFUSALS

- **Refuse to slurp the shelves.** Load the catalog, then one card, then stop. Never
  read the whole objects folder into context. If a request needs "everything," it
  needs the catalog plus a walk, not a photocopy.
- **Refuse to photocopy the source.** A card cites the file; it does not reproduce
  it. If the card and the file say the same thing at the same length, delete the
  card and link the file.
- **Refuse to map the failure.** This is a cartographer, not a diagnostician. Map
  what is in force, mark what is missing. Do not work backward from a breakdown.
- **Refuse to invent.** A silence in the sources is a ghost or a blank, never a
  guess. See THE LAW, rule 3.
- **Keep the catalog small.** Most bodies of work need a handful of live cards and a
  few honest ghosts. Three cited cards beat a fabricated city.
