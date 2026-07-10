# User stories

## Roles

This document is **not role-agnostic**. Both corpus roles appear in every
functional entry: the human trader (actor, initiates interactions) and the
Technical Trader Solution (instrument, responds). No other actor appears in
functional content.

## Definitions

No doc-specific definitions beyond the corpus glossary. All specialized terms
used below (theme, candidate net, sync rank, bond, pair bond, etc.) are
defined in `digest-aids/glossary.md`.

## Entries

### US-001 — Daily Sync-Rank / Performance View

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I open my daily view. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I see every theme positioned by its
current sync rank and its recent performance (5D, 10D, 21D, and 62D, as
ADR-normalized theme averages), replacing a separately maintained watchlist.
For each theme I can see its label, member count, and performance dispersion
across members. I can toggle between viewing all members and viewing only
the top 50% most tightly bonded members, so I can tell whether a theme's
bonding is broad or concentrated in a tight core with a looser periphery.
`</rule>`
<!-- src: belief/correlation-framework.md L247-267 -->

**Non-functional:** None sourced.

---

### US-002 — Connection Research Surface

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I open the connection research
surface. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I see newly detected pair bonds
grouped into three situations: isolated (neither ticker belongs to or bonds
with any theme — a potential new theme seed), overlapping (one or both
tickers already belong to a theme — possible theme growth or a separate,
overlapping theme), and adjacent (a non-member ticker bonds to a theme
member — a candidate for addition to that theme). For each bonded pair I can
see the bonded tickers, their bond strength, which sync signal types are
driving it, and their relationships to existing themes. `</rule>`
<!-- src: belief/correlation-framework.md L309-311, L314-326 -->

**Non-functional:** None sourced.

---

### US-003 — Shared Theme Connection Analysis

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I request shared theme
connection analysis on a candidate net. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I receive two outputs: the top
candidate shared theme connections for that candidate net — possibly more
than one alternative connection for the same tickers — and a list of
additional plausible members: tickers consistent with a proposed connection
that have not yet shown the bonding signal but are worth monitoring, shown
assessable alongside the already-bonded tickers. This same analysis is
available whether I am investigating a brand-new candidate net or looking to
enrich an existing theme. `</rule>`
<!-- src: belief/correlation-framework.md L328-338; belief/filtering-logic.md L57-60 -->

**Non-functional:** None sourced.

---

### US-004 — Persistent Per-Theme Discard Decisions

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I review a ticker in the
context of a specific theme and decide it does not belong. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can record that decision, and it
persists until I explicitly reverse it. Discarding a ticker for one theme has
no effect on its consideration for any other theme. `</rule>`
<!-- src: belief/correlation-framework.md L340-343 -->

**Non-functional:** None sourced.

---

### US-005 — Free-Form Bond Network Exploration

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I select any ticker to explore
its bonds, at any time, independent of my daily view. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can see what that ticker bonds to,
then continue from any bonded ticker to see what it in turn bonds to, moving
freely through the bond network. `</rule>`
<!-- src: belief/correlation-framework.md L345-348 -->

**Non-functional:** None sourced.

---

### US-006 — Continuous Theme Maintenance Suggestions

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I review my themes. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I see ongoing suggestions for tickers
to add (based on new bonding to existing members) and tickers to consider
removing (based on fading bonding to the rest of the theme), and I can
confirm or reject each suggestion individually. `</rule>`
<!-- src: belief/correlation-framework.md L354-358 -->

**Non-functional:** None sourced.

---

### US-007 — Per-Theme Deep-Dive Assessment

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I open a specific theme from my
daily view. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can inspect the recent chart
behavior of the theme's members side by side, see a per-ticker breakdown of
how much each member is contributing to the theme's overall bonding strength,
and see a breakdown of what is driving that bonding (which sync signal types
and, for structural resemblance, which timeframes). This lets me distinguish
a tightly bonded core from a looser periphery, and lets me visually verify
that the observed resemblance holds up in the actual charts before I rely on
it. `</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §2.1, §2.2, §2.3 (aggregated) -->

**Non-functional:** None sourced.

---

### US-008 — Pending-Action Awareness at Session Start

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I begin my daily session.
`</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I see, without having to scan for
them, which themes have accumulated pending review items (new bonds involving
members, pending add/remove suggestions, bonding-strength shifts) since I
last worked, and how many newly detected pair bonds involve tickers not yet
belonging to any theme. I can enter the relevant review surface directly
from each notification. `</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §1.2 -->

**Non-functional:** None sourced.

---

### US-009 — Session-Start Data-Freshness Confirmation

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` Before I act on anything in the daily
view. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can confirm that the underlying
observations reflect the most recent completed trading day, so that I know I
am not deciding against a stale snapshot. If the underlying data is older
than expected, I am warned before I start. `</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §1.3 -->

**Non-functional:** None sourced. *(No MB-### grounding — operational outcome;
trader-confirmed as a legitimate corpus entry despite lacking a market-behavior
motivation, per us-snapshot-extract.md Table B row `c`.)*

---

### US-010 — Confirm a Connection and Create a Theme from a Candidate Net

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I am reviewing a candidate net
(from the connection research surface described in US-002, or from a shared
theme connection analysis as in US-003) and I decide the proposed connection
is meaningful. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can confirm the proposed connection
(or write my own connection description in its place), select which of the
currently bonded tickers become the initial members of the new theme, and
optionally include analysis-suggested additional tickers as initial members
at the same time. Tickers I do not include remain visible in the underlying
bond network for further consideration. The result is a new theme carrying
its confirmed connection and its initial members. `</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §3.3 -->

**Non-functional:** None sourced.

---

### US-011 — Ad-Hoc Connection Analysis on a Trader-Supplied Ticker List

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I have a list of tickers I want
to investigate for a possible shared connection, at any time and independent
of what the daily bond network is currently showing. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can submit that ticker list on
demand and receive shared theme connection analysis for it (see US-003 for
what the analysis returns), without waiting for the tickers to first show up
as a candidate net in the daily bond network, and independent of whether the
tickers currently show any bonding at all. `</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §3.6 -->

**Non-functional:** None sourced.

---

### US-012 — Interactive Detection-Sensitivity Control

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I am reviewing the current set of
newly detected pair bonds and want to explore what the picture looks like
under stricter or looser detection criteria than the default. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can adjust detection strictness
interactively — becoming more strict or less strict than the default — and
see the resulting revised set of detected bonds immediately, without waiting
for the underlying detection to be re-run from scratch. The adjustment is
exploratory: it does not persist beyond my session and does not overwrite
the default detection result the rest of the workflow (badges, maintenance
queue, downstream analysis) is based on. `</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §3.7 -->

**Non-functional:** None sourced. *(No MB-### grounding — exploration/research
control; trader-confirmed as a legitimate corpus entry, per us-snapshot-extract.md
Table B row `f`.)*

---

### US-013 — Full Trader Discretion Over Theme Membership at Any Time

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` At any time, in any context in which I
am looking at a theme or at a ticker. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I can add any eligible ticker to any
theme, or remove any current member from any theme, regardless of what any
analysis or suggestion is currently indicating and regardless of which
surface I am working in. My discretion is not gated by any analysis output
— the analysis is one input among several I may act on (see STR-006).
`</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §4.3; foundational principle P8 -->

**Non-functional:** None sourced.

---

### US-014 — Periodic New-Ticker Onboarding Review

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When a set of newly eligible tickers
has entered the universe (typically after a periodic universe refresh).
`</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I review those tickers together with
supporting business context (a short business description, recent catalysts,
notable findings about the company, and characterization of the ticker's
products, services, and any distinctive technology) and any theme-assignment
suggestions the system has for them, so that I can efficiently onboard the
new tickers into existing themes where they fit. `</rule>`
<!-- src: snapshot/2026-07-02/cockpit-user-stories.md §4B.1 -->

**Non-functional:** None sourced. *(No MB-### grounding — workflow support;
trader-confirmed as a legitimate corpus entry, per us-snapshot-extract.md
Table B row `p`.)*

---


### US-015 — Narrative-Cluster Discovery Surface

**Actor:** `<rule strictness="hard">` human trader `</rule>`

**Action:** `<rule strictness="hard">` When I review narrative/topic findings
drawn from earnings reports, SEC filings, and news coverage. `</rule>`

**Instrument:** `<rule strictness="hard">` Technical Trader Solution `</rule>`

**Outcome:** `<rule strictness="hard">` I see tickers grouped into clusters by
shared or adjacent narrative, independent of whether any pair bond or sync
signal exists between them, and independent of whether they already belong
to a theme. For each cluster I can see which storyline or topic ties it
together, and how its frequency of mention or company breadth is trending.
From a cluster I can move directly into a side by side chart inspection of
its members to assess whether to create a theme from it (see STR-011).
`</rule>`
<!-- src: STR-011; market-behavior.md MB-013 -->

**Non-functional:** None sourced.

---

## Open items

None.

## Change log

- v0.4 (2026-07-07) — new entry US-015 (Narrative-Cluster Discovery
  Surface), the trader-facing counterpart to STR-011 (Narrative-Led Cluster
  Discovery, Chart-Confirmed into a Theme) — groups tickers by shared or
  adjacent narrative independent of bonding/sync status, surfaces
  mention-frequency/company-breadth trend per cluster, and hands off into
  side-by-side chart inspection for theme-creation judgment. Note: US-015
  reuses an ID previously assigned-then-withdrawn in Session 11 (Chapter 8
  model-improvement row `q`, returned to Table B-deferred); this is an
  unrelated new entry, not a revival of that withdrawn content.
- v0.3 (2026-07-06) — Session 11: authored US-007–014 from
  `docu\us-snapshot-extract.md` Table B (8 entries: rows a, b, c, d, e, f,
  o, p), aggregating `cockpit-user-stories.md` snapshot items at a higher
  level per client-project requirements — GUI/dev/tech-implementation
  mechanics removed, trader-facing outcomes retained. Row `q` (Continuous
  Improvement of the Pattern-Resemblance Detection) was initially authored
  as US-015 and then withdrawn by trader on further consideration this
  session — moved back to Table B-deferred in the extract; not needed at
  this time. Screening artifact (`us-snapshot-extract.md`) records
  duplicates absorbed into US-001–006 or routed to MB/STR (Table A), rows
  deferred by trader instruction to a possible later authoring pass
  (Table B-deferred, now rows g–n and q), and drops with reasons (Table C).
  Three entries (US-009, US-012, US-014) lack MB-### grounding and are
  trader-confirmed as legitimate corpus outcomes despite it, flagged inline
  in each entry's Non-functional field. This snapshot pass departs from
  `snapshot-transfer.md` (used for all six `belief/` files) because the
  cockpit-user-stories snapshot is a mature DEV-project artifact whose
  granular implementation-tied stories would produce structurally
  incompatible input content if transferred row-by-row.
- v0.2 (2026-07-06) — belief/ remaining-files routing+authoring pass
  (filtering-logic.md). Expanded US-003 (added filtering-logic.md source
  anchor — reinforcing duplicate, no content change).
- v0.1 (2026-07-06) — initial draft: 6 entries (US-001–006) authored from
  `snapshot-routing.md` §3 rows (correlation-framework.md), per
  user-story-authoring v0.3 and authoring-hygiene v0.10. Several adjacent
  routing rows were merged into single entries where they describe one
  coherent capability rather than separate actions (e.g. US-002 merges the
  research-surface-exists row with the bond-situation-categorization and
  per-situation-detail rows; US-003 merges the connection-analysis row with
  its two-output row and the new-vs-existing-theme scope note). Tech-worded
  source phrasing ("AI reasoning" / "AI reasoning workflow") rewritten as
  "shared theme connection analysis" per Rule 10 substitution, approved
  under Rule 16 this session.
