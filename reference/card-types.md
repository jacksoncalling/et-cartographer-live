# Card Types — the closed set

> This is the catalog's grammar, not the catalog. Six noun types, a small set of
> movements, two evaluative layers. A card cites its source. The source file wins;
> if a card and the real document disagree, the card is wrong.
>
> Territory: the Einstein Telescope Euregio ecosystem (DE / BE / NL three-country
> corner). Later reader: a new ecosystem-builder or a cold model joining the
> cross-border coordination work, who must not re-derive the whole tangle.

---

## The 6 nouns

Every object on a shelf is exactly one of these. If a candidate is not one of
these, it is a movement, a tension, or a gradient — not a card.

### 1. Actor
An entity that can **hold** a capability, **receive** funds, **sign** an
instrument, or **make** a decision.
- subtype (in-card, not a new type): research institution | industry firm |
  government body | agency | consortium
- home jurisdiction
- fields: what it holds, what it has signed, what it receives

### 2. Capability
A concrete technical or organizational capacity, tied to a holder. Technology
counts here (a capability someone can exercise), a wish does not.
- holder (an Actor) — a capability with no holder is a **ghost**
- depends-on (other capabilities or resources)

### 3. Shared Resource
The heavy commons multiple Actors use: the instrument (the telescope itself),
the site, pooled funds, shared data.
- governed-by (a Jurisdiction)
- funded-by (Instruments) — does money actually reach it?

### 4. Instrument
Any formal device that **binds or enables**. This is where permits, zoning,
taxation, grants, contracts, MOUs and treaties live — one type, many kinds.
- kind: contract | MOU | grant | permit | zoning designation | tax arrangement | treaty
- jurisdiction (which authority issues / enforces it)
- parties (the Actors bound or enabled)
- **binding strength**: treaty > contract > grant agreement > MOU > pledge > assumed
  (this attribute carries your Contract-vs-Commitment distinction)
- **money-routing**: does € actually flow across the border through this, or is it
  named but dry?
- status: live | pending | leftover | ghost (see below)

### 5. Decision
A governance choice already made.
- decider (an Actor or body)
- **subsidiarity scale**: local | regional | national | EU | cross-border
- **mandate status**: is the decider actually authorized at that scale, or is the
  authority assumed? (an assumed mandate is a ghost)
- commits (what it now locks) / supersedes (what it replaces)

### 6. Jurisdiction
A territorial or legal authority envelope. First-class because in a three-country
project, "whose law / whose tax / whose permit applies" decides everything.
- authority type: national (NL/BE/DE) | provincial | EU | Euregio | claimed sovereign zone
- governs: which Instruments, Resources, Decisions fall under it
- the hard question it answers or dodges: for a shared object hosted in one
  country, whose permit, whose tax base, whose law?

---

## Movements (how nouns move) — closed set

- **holds** — Actor → Capability
- **binds / enables** — Instrument → Actors, Resource
- **governs** — Jurisdiction → Instrument, Resource, Decision
- **routes-funds-to** — Instrument → Actor, Resource (the liquidity question)
- **depends-on** — Capability → Capability, Resource → Instrument
- **decides / supersedes** — Decision → anything
- **contested-by** — any noun → a Tension

---

## Live / Pending / Leftover / Ghost — the marking rule

Every card carries one. This is the tripwire discipline: a cold reader, human or
model, must never implement a wish as if it were wired.

- **Live** — wired now, citeable to a current source. A signed instrument, a named
  holder, money actually routing, an authority actually exercising it.
  *e.g. a grant agreement currently disbursing; a zoning study commissioned and underway.*
- **Pending** — forthcoming and sourced as such, not yet wired, on a credible track to
  live. *e.g. a bidbook in preparation; a site decision on a set timeline but not yet
  made.* Not a ghost (a ghost has no sourced path) and not a leftover (a leftover was
  once live).
- **Leftover** — honest residue. Was live, still referenced, no longer load-bearing.
  *e.g. an MOU from the feasibility phase whose signatory agency was reorganized;
  a capability mapped from the reference detector that does not transfer to this site.*
- **Ghost** — a name with no wiring. Everyone references it; no Actor holds it, no
  Instrument binds it, no Jurisdiction governs it, no money routes through it.
  A ghost is a tripwire, not a lie — mark it, do not delete it.
  *e.g. the **claimed sovereign zone** for the telescope (named in conversation, no
  legal instrument, no authority holds it); the **cross-border funding vehicle**
  everyone cites that nothing routes through yet; a **joint governance body** with
  no signed mandate.*

> Why this rule exists: an agent once fabricated a whole interview because a name
> in its graph had no wiring and it filled the gap. A ghost mapped as live is how
> the next reader, or the next model, builds the wrong world.

---

## Evaluative layer — Terroir's brain, ported

### Tension (a structural conflict, both sides live now)
Both sides pull, neither can be fully satisfied, and solving everything else would
not dissolve it.
*e.g. "Host-nation siting concentrates permits, tax base and prestige in one
country, while equal cross-border funding requires all three to contribute
equally — one side ends up subsidizing the other's sovereignty."*

### Gradient (a directional pressure with a cost and a threshold)
Direction (toward / away_from / protecting), what it trades off, and the tipping
point it approaches.
*e.g. "Moving toward a single host jurisdiction, at the cost of the durability of
the non-host parliaments' budget commitments; threshold: the point where a
non-host government can no longer justify contribution to its own taxpayers."*

---

## What every card must end with: Hits / Does not hit

- **Hits** — the objects that move if you change this one.
- **Does not hit** — the obvious wrong neighbour, the word everyone reaches for
  that this change does *not* touch. Without this line, a card is a glossary entry.

*Worked example — card "Site zoning designation (NL Limburg)" [Instrument · kind:
zoning · status: partial/leftover]:*
- **Hits:** deep-civil-works Capability; the environmental permit Instrument; the
  host Jurisdiction's tax base; the site Shared Resource.
- **Does not hit:** the cryogenics and optics Capabilities. The obvious wrong
  neighbour is "it's one project, so zoning must touch the science too." It does
  not. The physics is site-agnostic until civil works begin.

---

## What every card must also end with: a Source line

After Hits / Does not hit, every card carries a **Source line** citing the smallest
openable locator, so a reader can check the claim in one hop. The grammar (URL vs
internal document, the per-type locators, the optional inline `[S#]` tags and
`verified:` stamp) is `reference/source-types.md`. The build reads this line and
renders it as clickable links on the card, using the map's `repo_base`.

```
Source: scripts/rank.py:96-175 ; profil/kanon.md
Source: https://youtu.be/OtkM18P1GeE?t=42 · verified: 2026-09-02
Source: interview-2026-08-16.md [00:14:32] "cruising to big clients"
```

A card with no Source line is not finished. A card whose Source names only a
container ("the repo", "the interview") is not cited, it is labelled.

---

## Naming collisions in this territory (write them down — required)

- **Node** — Bauwens' "excellent node" (a whole institution/community) vs a graph
  node vs a network node vs a detector node of the interferometer.
- **Commitment** — a signed legal commitment (Instrument, high binding) vs
  Ruddick's "commitment pooling" (a liquidity mechanism) vs a soft political pledge
  (leftover/ghost).
- **Federation** — political federalism (a state form) vs P4P con-federation
  (infrastructure-sharing) vs an EU "federated" funding call.
- **Host** — the host nation (sovereignty) vs a host institution (admin) vs a
  hosting facility (physical site).
- **Grant** — an EU structural grant vs a national research grant vs a regional
  development grant. Different jurisdiction, different rules, different
  money-routing. "Who gets the grant money" hides this collision.

---

## Walk order (how a cold reader enters)

1. Start at the **catalog** (the front door), never here and never the objects folder.
2. Ask **one** question ("who can actually do the deep civil works?" → open that
   Capability card; "does money cross the border?" → open that Instrument card).
3. Read that **one** card: what it is, why it's shaped that way, its status, what it
   hits and does not hit.
4. **Stop.** Do not load the rest.
