# Source Types — what a citation is, and how deep it points

> Every card cites its source (THE LAW, rule 1, in `rules.md`). This file defines
> what counts as a source and how granular the citation must be. The card grammar
> (the 6 nouns, the movements) lives in `card-types.md`; this file governs the
> **Source line** that every card ends with.
>
> One test decides everything here: **can a reader open the source and check the
> claim without reading the whole thing?** If yes, it is a citation. If they land
> on a container (a whole interview, a domain, a 40-file repo) and still have to
> hunt, it is a label, and a label is not a source.

---

## The unit of a citation: the smallest openable locator

A citation names the **smallest thing a reader can open and verify**, not the box
it lives in. "Interview 1" is the box. `interview-2026-08-16.md [00:14:32]
"cruising to big clients"` is the locator. Always cite the locator.

This is the same discipline a journal article uses: a claim carries an inline
citation to a specific page or passage, and the reference list at the foot resolves
it. The card's description is the prose; the **Source line** is the reference list.

---

## The two kinds of source (both first-class, both must resolve)

### 1. External source — a URL

A public web resource. Cite the URL, **deep-linked to the passage**, never just the
domain or the home page.

| Resource | Cite | Not |
|---|---|---|
| Web page | `https://site.org/report#financing` | `https://site.org` |
| Video / audio | `https://youtu.be/ID?t=830` (timestamp) | `https://youtu.be/ID` |
| Paper | the DOI URL, plus `p.12` or `§3.2` if quoting | "the Nature paper" |
| Registry / dataset | the row or query URL | "their member list" |

### 2. Internal source — a document that ships with or beside the map

A file in the repo, the vault, or an inbox: code, notes, a PDF, a transcript. Cite
the **path plus a locator matched to the file type**:

| File type | Locator | Example |
|---|---|---|
| Code | `path:line` or `path:start-end` | `scripts/rank.py:147-175` |
| Markdown / docs | `path#heading` | `HANDOFF.md#known-gaps` |
| PDF | `path p.N` or `path §N` | `bidbook.pdf p.44` |
| **Transcript / interview / voice note** | `path` + **timestamp or speaker-turn** + **a short verbatim quote** (≤ ~12 words) | `interview-2026-08-16.md [00:14:32] "cruising to big clients"` |
| Spreadsheet / registry | `path!Sheet:cell` or the row key | `suppliers.csv row 41` |

**Why the transcript gets a quote as well as an address.** A timestamp tells the
reader where to look; the verbatim quote is what they check the claim against, and
it is the anchor that survives if the file is re-ordered and line numbers move. For
anything spoken, cite the moment and the words, never just the meeting.

**When the internal source is private.** The map may point at a document a judge or
a cold reader cannot open (a client transcript, a private repo). The citation is
still written to the locator, and the territory is made openable one of three ways
(the field's three solutions): pin the territory in the repo, ship a generated index
instead of the source, or ship excerpt files so the private tree never opens. The
map that ships **inside** the repo it maps (as the Kustos run does) resolves this by
construction: every `path:line` opens for anyone who clones it.

---

## Granularity: cite the moment, not the container

The one rule, stated as a gate: **a reader must get from the card to the exact
passage in one hop.** Apply it per source type:

- A whole document is too coarse. Add the line, heading, page, or timestamp.
- A domain is too coarse. Add the path or the anchor.
- A meeting is too coarse. Add the timestamp and the quote.
- A repository is too coarse. Add the file and the line.

If you cannot point that precisely, the honest citation is the locator you *do*
have plus `verified: open` (see below), which says "this is as deep as the evidence
goes, and it is not yet checked." That is a research question, not a finished card.

---

## Multi-source cards: the inline-tag model (optional)

Most cards pull from one place and need only a single `Source:` line. When a card
genuinely blends sources, mark each claim inline and resolve the tags at the foot,
exactly like footnotes:

```
# Rank

Assigns an evidence level from publication type [S1], then scores by topic match,
journal trust, recency, and kanon overlap [S2].

...movements...

- **Hits:** ...
- **Does not hit:** ...

Source:
  [S1] scripts/rank.py:40-95
  [S2] scripts/rank.py:96-175 ; profil/kanon.md
```

Default to the single line. Reach for tags only when a reader would otherwise not
know which sentence came from where.

---

## The verification stamp (optional, recommended on living territories)

A territory that changes (a live account, a codebase, an inbox) needs its cards
dated, so a reader knows how stale a claim might be. Append to any citation:

```
Source: gohighlevel account "Parent Intake" workflow #7 · verified: 2026-08-18 · by: Sadie (VA)
```

- `verified: YYYY-MM-DD` — when the card was last checked against the source.
- `by: <who or what>` — the human or the checker that confirmed it (optional).

This is what makes "the file wins" enforceable: a card that disagrees with the
source is not a matter of opinion, it is out of date, and the stamp says since when.
On a static, cited-from-public-documents territory the stamp is optional; on a live
one it is the difference between a map and a guess.

---

## What the tools do with the Source line

`tools/build-artifact.py` reads the `Source:` line of each card and renders it as a
**Source block** on the card, with the locators turned into clickable links:

- A **URL** becomes a link to itself.
- An **internal `path:line`** becomes a link to that file at that line, using the
  `repo_base` set in the map's `build.json` (e.g. a GitHub blob URL). With no
  `repo_base`, the path renders as plain text (still a valid citation, just not
  clickable).

So the citation a reader sees is not a footnote they must trust; it is a door they
can open. That is the whole point: **the card cites the source, the source is one
click away, and if they disagree, the file wins.**

---

## The refusals (carried from `rules.md`)

- **No source, no card.** A claim with no locator does not get written as a fact.
- **A container is not a citation.** "The interview", "the repo", "their site" fail
  the one-hop test. Add the locator or mark the card `UNVERIFIED`.
- **Do not photocopy the source into the card.** The citation points; it does not
  reproduce. A short verbatim quote is an anchor; a pasted paragraph is a photocopy.
