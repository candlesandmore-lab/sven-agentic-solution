# Trading strategies

## Roles

This document is **role-agnostic**. Entries describe what exploitation of a
market behavior looks like, not what the human trader or the Technical Trader
Solution do to support it. What the Technical Trader Solution surfaces to
support these strategies is described in `user-stories.md`, not here.

## Definitions

No doc-specific definitions beyond the corpus glossary. All specialized terms
used below (sync rank, theme, candidate net, pair bond, bond cohort, setup,
conviction, etc.) are defined in `digest-aids/glossary.md`.

## Entries

### STR-001 — Morning Sync-Rank Workflow

**Exploited behavior:** `<observation>` Exploits MB-006 (Sync Rank Formation)
and MB-005 (Sync and Theme Development Is Independent of Price-Movement
Timing). Sync rank identifies bonded themes worth daily review, but a high
sync rank alone does not indicate a move is imminent or predictable (MB-005)
— chart confirmation is required before any trade is considered.
`</observation>`
<!-- src: belief/correlation-framework.md L294-302 -->

**Trigger conditions:** `<rule strictness="hard">` (a) Scan for themes with
high sync rank at low-to-medium recent performance. (b) Within each candidate
theme, filter to the strongest-bonded cohort (core and strong-tier members).
(c) Inspect those tickers' charts directly. (d) Proceed only if an actionable
setup (tightening range, flag, base) is present in the charts — assessed by
trader judgment, never automated. `</rule>`
<!-- src: belief/correlation-framework.md L294-302 -->

---

### STR-002 — Sync-Rank / Performance Zone Interpretation

**Exploited behavior:** `<observation>` Exploits MB-006 and MB-005. Reads the
combination of a theme's sync rank and recent performance to prioritize
review attention. `</observation>`
<!-- src: belief/correlation-framework.md L273-280 -->

**Trigger conditions:** `<rule strictness="hard">` (a) High sync rank +
low-to-medium performance → highest-priority review; flags tickers likely
invisible to conventional momentum screening — not a claim that a move is
imminent (MB-005). (b) High sync rank + high performance → treat as probably
late; check for un-moved laggards in the strongest cohort, or a new
synchronized setup forming across the theme. (c) Low sync rank + high
performance → treat as a broad-market move, not theme-specific. (d) Low sync
rank + low performance → not actionable. `</rule>`
<!-- src: belief/correlation-framework.md L273-280 -->

---

### STR-003 — Dispersion as a Regime-Dependent Risk Gauge

**Exploited behavior:** `<observation>` Exploits MB-006 (sync rank) and MB-007
(Pairs Bond, Groups Emerge from Bonded Pairs — cohesion looseness).
Performance dispersion among a theme's members carries opposite implications
depending on the prevailing market regime. `</observation>`
<!-- src: belief/correlation-framework.md L282-288 -->

**Trigger conditions:** `<rule strictness="hard">` (a) In a broadly rising
market, wide performance dispersion within a high-sync theme is read as a
tradeable-laggard opportunity. (b) In a normal market, the same wide
dispersion is read as a fragility warning — a loosely bonded theme is more
likely to break apart than for laggards to catch up. `</rule>`
<!-- src: belief/correlation-framework.md L282-288 -->

---

### STR-004 — Bonding Signal Sustains Investigation Without Confirmation

**Exploited behavior:** `<observation>` Exploits MB-004 (Unified Sync
Activation). Any sync-type activation between two tickers is sufficient
grounds to keep them under active consideration while their connection is
investigated, even before a theme is confirmed. `</observation>`
<!-- src: belief/correlation-framework.md L311-312; belief/filtering-logic.md L50-52 -->

**Trigger conditions:** `<rule strictness="hard">` A pair bond is active
(any sync type) AND the connection between the pair has not yet been
confirmed or rejected → the tickers remain under consideration. `</rule>`
<!-- src: belief/correlation-framework.md L311-312 -->

---

### STR-005 — Theme Membership Follows Bonding, Not a Fixed Schedule

**Exploited behavior:** `<observation>` Exploits MB-007. Since themes emerge
and evolve from bonded pairs rather than being declared once, membership is
continuously reviewable rather than fixed at formation. `</observation>`
<!-- src: belief/correlation-framework.md L354-358 -->

**Trigger conditions:** `<rule strictness="hard">` (a) A new ticker begins
bonding to existing theme members over a sustained period → candidate for
addition, pending trader confirmation. (b) An existing member's bonding to
the rest of the theme fades over a sustained period → candidate for removal,
pending trader confirmation. `</rule>`
<!-- src: belief/correlation-framework.md L354-358 -->

---

### STR-006 — Theme Membership Is a Discretionary Trader Decision

**Exploited behavior:** `<observation>` Exploits MB-004 — bonding signals are
one input among several the trader may act on. The trader retains sole
authority over theme membership regardless of which input surfaced the
ticker. `</observation>`
<!-- src: belief/correlation-framework.md L360-362 -->

**Trigger conditions:** `<rule strictness="hard">` A ticker may be added to a
theme on the basis of a bonding signal, a connection hypothesis surfaced
through analysis, external research, personal knowledge, or any other input
the trader considers relevant — no single input source is required or
sufficient on its own. `</rule>`
<!-- src: belief/correlation-framework.md L360-362 -->

---

### STR-007 — Weakened Bonding Does Not Automatically Remove a Theme Member

**Exploited behavior:** `<observation>` Exploits MB-007. Since bonding
strength naturally fluctuates, a fade in bonding — or a member falling below
screening filters — is not treated as a removal trigger on its own.
`</observation>`
<!-- src: belief/correlation-framework.md L364-367 -->

**Trigger conditions:** `<rule strictness="hard">` A theme member's bonding
to the group weakens, or the member's characteristics change (e.g. falls
below screening filters) → this is an input to the trader's removal
judgment, not an automatic removal condition; the member may remain in the
theme. `</rule>`
<!-- src: belief/correlation-framework.md L364-367 -->

---

### STR-008 — Sync Rank as Conviction Modifier

**Exploited behavior:** `<observation>` Exploits MB-006. Sync rank adjusts
how much setup quality the trader requires before acting, without replacing
setup quality as the actual trigger. `</observation>`
<!-- src: belief/correlation-framework.md L373-378 -->

**Trigger conditions:** `<rule strictness="hard">` (a) High sync rank +
confirmed connection → setups the trader would otherwise skip become
acceptable. (b) Lower sync rank + hypothesized (unconfirmed) connection →
only the highest-quality setups are acted on. `</rule>`
<!-- src: belief/correlation-framework.md L373-378 -->

### STR-009 — Break-Confirmed Entry, Staged by Mover Order

**Exploited behavior:** `<observation>` Exploits MB-006 (Sync Rank Formation)
and MB-015 (Theme Lifecycle Overview, corrected relationship): sync/theme
tracking narrows which tickers the trader monitors for chart-level setups —
it carries no timing signal for when a setup will resolve. Entry is
exploited independently, strictly at the point a monitored ticker's chart
shows a confirmed break out of consolidation — an event unrelated to the
theme's bonding-lifecycle state. Each subsequent confirmed mover carries
lower risk and lower reward than the one before it, and raises conviction
that the underlying setup is genuinely activating (see Mover order,
glossary). `</observation>`
<!-- src: belief/filtering-logic.md L117-136 -->

**Trigger conditions:** `<rule strictness="hard">` (a) The trader acts only
once a ticker's break out of consolidation is confirmed — never in
anticipation of it; anticipating the break before it happens is an
established loss pattern. (b) Acting on the first mover carries the highest
reward and the highest relative risk, since no other member's break yet
confirms the setup is activating. (c) Acting on the second or third mover
carries progressively lower risk and lower reward than the mover before it,
since each prior confirmed break is itself further confirmation; how many
subsequent movers the trader still acts on depends on overall market
conditions. `</rule>`
<!-- src: belief/filtering-logic.md L123-136 -->

---

### STR-010 — Prioritize Discovery Workflow Over Momentum Screening for Early/Unlabeled Themes

**Exploited behavior:** `<observation>` Exploits MB-016 (Theme Lifecycle:
Formation): theme formation begins from a single pair bond or narrative
convergence, before tickers typically meet momentum-screening criteria.
Momentum- and rank-based screening therefore structurally excludes tickers
in formation and early-strengthening states, and provides no path to
visibility at all for themes carrying no existing label. `</observation>`
<!-- src: belief/filtering-logic.md L142-171, L177-189 -->

**Trigger conditions:** `<rule strictness="hard">` (a) For themes already
known and tracked but not yet meeting momentum criteria, the trader
monitors sync-rank/bonding data directly rather than waiting for momentum
screening to surface them. (b) For candidates carrying no existing theme
label, the trader relies on candidate-net and connection-discovery output
(see user-stories.md) rather than momentum screening, since no rank-based
mechanism exists to surface an unlabeled theme. `</rule>`
<!-- src: belief/filtering-logic.md L177-189 -->

### STR-011 — Narrative-Led Cluster Discovery, Chart-Confirmed into a Theme (Text-First Path)

**Exploited behavior:** `<observation>` Exploits MB-013 (Narrative Formation):
a common storyline or topic surfacing with increasing frequency, or across a
growing number of companies, in earnings reports, SEC filings, and news
coverage is a text-based signal that can precede any sync-threshold
crossing — the reverse of the usual sync-first path; per-ticker narrative
findings narrow the search for what connects a group of tickers independent
of how the group first surfaced. Also exploits MB-007 (a confirmed connection
is a theme's minimum seed, whether the candidate arrived via pair bond or via
narrative) and MB-006 (Sync Rank Formation) — once formed, a narrative-led
theme is tracked with a sync rank alongside every other theme, with no
separate category for how it originated. `</observation>`
<!-- src: market-behavior.md MB-013, MB-007, MB-006 -->

**Trigger conditions:** `<rule strictness="hard">` (a) Regularly review a
group of tickers' earnings call transcripts, SEC filings, and news coverage;
surface any storyline or topic whose frequency of mention, or the number of
companies carrying it, is increasing — independent of any price action
(MB-013). (b) Cluster tickers sharing the same or an adjacent narrative into
a candidate group, even where no pair bond or sync signal yet exists between
them (MB-013's reverse path). (c) Inspect the charts of the clustered
tickers directly; create a theme only once a sufficient portion of the
cluster shows a similar rhythm, price direction, or other discretionary
chart characteristic — trader judgment, never automated. Narrative strength
alone never creates a theme (MB-013's scope caveat: narrative does not
indicate price direction). (d) Once created, track the theme and its sync
rank alongside every other theme (MB-006) — a narrative-led origin does not
exempt it from ongoing sync-rank tracking. `</rule>`
<!-- src: market-behavior.md MB-013, MB-007, MB-006 -->

---

## Open items

None. All entries cite at least one MB-###; no unresolved dependencies.

## Change log

- v0.7 (2026-07-07) — new entry STR-011 (Narrative-Led Cluster Discovery,
  Chart-Confirmed into a Theme — Text-First Path), grounded on MB-013
  (Narrative Formation), MB-007 (minimum-seed concept extended from
  pair-bond to narrative-cluster origin), and MB-006 (Sync Rank Formation,
  for post-formation tracking). Trader-directed: this is the text-first
  sibling to the sync-first path already covered by STR-001/STR-005 —
  narrative convergence substitutes for the initial sync/bonding signal,
  with chart-level confirmation required before theme creation and ongoing
  sync-rank tracking applying identically once formed.
- v0.6 (2026-07-06) — updated STR-001's exploited-behavior text for MB-005's
  new title ("Sync and Theme Development Is Independent of Price-Movement
  Timing", was "Bonding Strength and Future Price Movement — Uncertain
  Relationship") — MB-005 was elevated in market-behavior.md v0.7 to be the
  corpus's canonical statement of the sync/price-timing-independence
  principle. No change to STR-001's own claims.
- v0.5 (2026-07-06) — cleanup pass: removed STR-006's "(Corrected
  2026-07-06...)" explanatory note — same "no client-facing value" category
  as STR-009's note, dropped in v0.4; the entry's Trigger conditions already
  stand on their own.
- v0.4 (2026-07-06) — trader review of manual market-behavior.md edits: (1)
  dropped STR-009's explanatory correction note (no client-facing value —
  the entry's own content already stands on its own). (2) New entry STR-010
  (Prioritize Discovery Workflow Over Momentum Screening for Early/Unlabeled
  Themes), converting former MB-021 (Screening-Based Blind Spot) — trader
  determined that entry described trader/screening practice, not market
  behavior, and belongs here instead; re-grounded on MB-016 (Formation)
  since MB-021 itself no longer exists to cite.
- v0.3 (2026-07-06) — trader-directed corrections following review of the
  belief/ remaining-files pass: (1) STR-006 reworded — its Trigger
  conditions had named the "shared theme connection analysis" capability by
  its US-003 name, violating STR's role-agnostic framing (STR entries must
  not reference what the Technical Trader Solution surfaces); reworded to a
  generic input-source description. (2) STR-009 re-grounded: originally
  cited theme-lifecycle phases (MB-018/MB-019) as the timing basis for
  break-confirmed entry; trader confirmed the source material's implicit
  link between price-movement timing and theme-lifecycle stage is a
  misconception. STR-009 now cites MB-006 and MB-015's corrected Scope
  caveat instead — the underlying break-confirmed/mover-order exploitation
  logic is unchanged and confirmed correct by the trader, only its MB
  grounding was wrong.
- v0.2 (2026-07-06) — belief/ remaining-files routing+authoring pass
  (filtering-logic.md). Expanded STR-004 (added filtering-logic.md source
  anchor — reinforcing duplicate, no content change; note: no "AI reasoning"
  substitution actually occurs in STR-004 — that phrase is dropped entirely
  as role-agnostic reframe, since STR content never names the Technical
  Trader Solution). New entry STR-009 (Break-Confirmed Entry, Staged by
  Mover Order).
- v0.1 (2026-07-06) — initial draft: 8 entries (STR-001–008) authored from
  `snapshot-routing.md` §3 rows (correlation-framework.md), per
  trading-strategy-authoring v0.3 and authoring-hygiene v0.10. §3.4's
  discard-decision permanence/independence content (routing row "§3.4 P
  L340–343 policy half") was folded into US-004's Outcome instead of drafted
  as a standalone STR entry — it describes persistence/scoping behavior of a
  Technical Trader Solution capability, not exploitation of a market
  behavior, and could not honestly cite an MB-### (Rule 8).
