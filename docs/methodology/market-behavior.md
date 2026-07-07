# Market behaviors

## Roles

This document is **role-agnostic**. It records observable market conditions only.
The human trader and the Technical Trader Solution do not appear as actors in any entry.
Responses to these behaviors belong in `trading-strategies.md`.

## Definitions

No doc-specific definitions beyond the corpus glossary. All specialized terms
used below (sync, Type 1/2/3, bonding, sync rank, theme, confluence, etc.) are
defined in `digest-aids/glossary.md`.

## Entries

### MB-001 — Type 1: Spike Co-activation

**Phenomenon:** `<observation>` Two or more tickers show sharp price and volume
spikes within ±2–3 days of each other, in the same direction. Volume on the
activation day is discrete and clearly above the recent average. `</observation>`
<!-- src: belief/correlation-framework.md L27-32 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06 — not present in the §2.1–2.2 source text for
Type 1; the same statement appears in the source for Type 3, see MB-003.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Same-direction price and volume
spikes across two or more tickers, within a ±2–3 day window, with discrete
above-average volume on the activation day. `</observation>`
<!-- src: belief/correlation-framework.md L27-32 -->

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>`

**Example:** `<example>` RGTI, IONQ, QBTS (quantum computing, 2024–2025) showed
same-date volume spikes across all three tickers. `</example>`
<!-- src: belief/correlation-framework.md L34-35 -->

*(member 1 of 3, set: sync signal types — see MB-002, MB-003)*

---

### MB-002 — Type 2: Momentum Density with Resemblance

**Phenomenon:** `<observation>` Sustained directional momentum with elevated
volume over multiple consecutive weeks. A discrete volume spike may also occur
within that elevated period. This is the higher-energy, directional version of
Type 3 structural resemblance and inherently includes its resemblance
component. `</observation>`
<!-- src: belief/correlation-framework.md L37-45 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06 — not present in the §2.1–2.2 source text for
Type 2; the same statement appears in the source for Type 3, see MB-003.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Volume elevated above the prior
average for multiple consecutive weeks, with price-action resemblance
appearing between tickers during that period — pairwise resemblance within a
larger group of tickers, not necessarily all members simultaneously.
Performance leaders within the group of tickers may show linear, steady
appreciation rather than a spike-and-consolidate shape. `</observation>`
<!-- src: belief/correlation-framework.md L37-45 -->

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>`

**Example:** `<example>` TSEM/SMTC, LWLG/AXTI, LITE/GLW pairs (optical AI
infrastructure sector, 2025) each showed pairwise resemblance driven by volume
density rather than discrete spikes. `</example>`
<!-- src: belief/correlation-framework.md L50-52 -->

*(member 2 of 3, set: sync signal types — see MB-001, MB-003)*

---

### MB-003 — Type 3: Structural Resemblance

**Phenomenon:** `<observation>` Two tickers show visually similar chart
structure during the same or adjacent periods — similar shape, rhythm, and
timing of pauses and pushes — regardless of absolute price magnitude.
`</observation>`
<!-- src: belief/correlation-framework.md L54-60 -->

**Conditions:** `<observation>` Market-condition agnostic: equally informative
during selling periods and buying periods. `</observation>`
<!-- src: belief/correlation-framework.md L58-59 -->

**Observable indicators:** `<observation>` Temporary, pairwise chart-shape
resemblance between two tickers; a shift of even a single session still
qualifies. `</observation>`
<!-- src: belief/correlation-framework.md L54-60 -->

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>`

**Example:** `<example>` DOCN, AKAM, ATEN (cloud edge providers, 2025–2026)
showed pairwise resemblance rotating between pairs — temporary parallels that
ceased and reappeared, shifted by a single session. `</example>`
<!-- src: belief/correlation-framework.md L62-63 -->

*(member 3 of 3, set: sync signal types — see MB-001, MB-002)*

---

### MB-004 — Unified Sync Activation

**Phenomenon:** `<observation>` Two or more tickers moving similarly during
the same period for a non-random reason is one underlying phenomenon; the
type of similarity that manifests varies (see MB-001, MB-002, MB-003).
`</observation>`
<!-- src: belief/correlation-framework.md L11-13 -->

**Conditions:** `<observation>` Each signal type can occur at any point in a
group of tickers' bonding, triggered by any cause — gradual accumulation,
external shock, surprise event, or narrative catalyst. A group of tickers can
express Type 1 on day one due to a sudden event, or show Type 3 for months
with no spike. `</observation>`
<!-- src: belief/correlation-framework.md L16-21 (resolved CLARIF-001) -->

**Observable indicators:** `<observation>` The three signal types (MB-001,
MB-002, MB-003) are independent expressions of bonding, not sequential
lifecycle stages; how the bond originated is not itself observable or
relevant — only whether it currently exists, and its strength, are.
`</observation>` `<observation>` The overlapping of different sync signal
types in time and intensity is itself a valuable observation, distinct from
any single type's presence alone. Different signal types confirm each other:
spike co-activation between two tickers is strengthened if structural
resemblance is also found between them in a separate period; multiple
independent signal types pointing at the same pair is stronger evidence than
any single type alone. Bonding evidence also accumulates continuously across
time — a pair bonded on a given day may have been trending toward bonding for
days or weeks beforehand. `</observation>`
<!-- src: belief/correlation-framework.md L16-21, L108-111, L124-129 -->

**Scope caveat:** `<out-of-scope>` Does not imply the three signal types
represent a sequence or progression — they are independent expressions of
bonding, not lifecycle stages, and observing one does not predict that
another will follow. `</out-of-scope>`
<!-- src: belief/correlation-framework.md L16-17 -->

*(parent framing entry for set: sync signal types — see MB-001, MB-002, MB-003)*

---

### MB-005 — Sync and Theme Development Is Independent of Price-Movement Timing

**Phenomenon:** `<observation>` No sync-derived measure — sync rank,
aggregate bonding strength, or theme lifecycle stage — indicates the timing
of any specific price movement. Instances of high bonding strength among a
group of tickers have sometimes preceded significant subsequent price moves
for that group of tickers; many price moves in a group of tickers have also
occurred without any prior elevated bonding-strength signal. `</observation>`
<!-- src: belief/correlation-framework.md L71-74 (resolved CLARIF-001), L98-102 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06 — not present in the §2.1–2.2 source text for
this entry; the same statement appears in the source for Type 3, see MB-003.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Sustained elevated bonding
strength across a group of tickers prior to a subsequent price move — though
this pattern is inconsistent; many moves show no such prior signal. A set of
tickers with high sync rank is worth continued observation, not itself an
actionable trigger. `</observation>`
<!-- src: belief/correlation-framework.md L71-74, L98-102 -->

**Scope caveat:** `<out-of-scope>` This is a hypothesis, not confirmed: sync
rank, aggregate bonding strength, and theme lifecycle stage are all treated
as descriptive of a group's current state only — never as predictors of
future price-move timing or direction — until further empirical evidence
accumulates. This is the corpus's canonical statement of that principle;
MB-006, MB-015, MB-018, and MB-019 reference this entry rather than restate
it. `</out-of-scope>`

---

### MB-006 — Sync Rank Formation

**Phenomenon:** `<observation>` Sync rank (bonding strength) is driven
primarily by structural resemblance — Type 2 and Type 3 signals. Volume
spikes (Type 1) contribute to sync rank but cannot drive it alone.
`</observation>`
<!-- src: belief/correlation-framework.md L84-86 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` A tight resemblance-based
configuration (flag or base) with no volume spikes ranks higher than a
configuration with strong volume spikes but no sustained resemblance.
`</observation>`
<!-- src: belief/correlation-framework.md L90-91 -->

**Scope caveat:** `<out-of-scope>` See MB-005: sync rank indicates current
bonding strength only, not the direction or timing of any future move. This
entry adds no caveat content beyond MB-005. `</out-of-scope>`
<!-- src: belief/correlation-framework.md L98-102 -->

**Example:** `<example>` The quantum computing tickers (RGTI, IONQ, QBTS)
showed high sync rank during a subsequent low-volatility consolidation period
with no spikes, driven by shared structural resemblance alone. `</example>`
<!-- src: belief/correlation-framework.md L93-96 (chart-annotation wording dropped) -->

*(cross-refs: MB-001–003 — which types drive it; MB-005 — canonical
price-timing independence statement)*

---

### MB-007 — Pairs Bond, Groups Emerge from Bonded Pairs

**Phenomenon:** `<observation>` A pair-level bond is the basic unit of
bonding. A bond cohort is not declared — it emerges from multiple bonded
pairs that share members (e.g., pairs A–B, B–C, and A–C bonded together
produce a three-ticker bond cohort). `</observation>` `<observation>` A pair
bond together with a confirmed connection is the minimum seed for a theme —
distinct from a bond cohort, which is structural only and requires no
connection. `</observation>`
<!-- src: belief/correlation-framework.md L117-122; belief/filtering-logic.md L57-58 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Multiple bonded pairs sharing
common members form a bond cohort. `</observation>`
<!-- src: belief/correlation-framework.md L117-122 -->

**Scope caveat:** `<out-of-scope>` Does not imply a connection is confirmed
— a connection is confirmed or hypothesized only after bonding is observed,
and remains a separate requirement from the bonding itself. A bond cohort is
not itself a candidate net or a theme. `</out-of-scope>`
<!-- src: belief/correlation-framework.md L121-122 -->

---

### MB-008 — Market Independence via Index Comparison

**Phenomenon:** `<observation>` Two tickers resembling each other while
diverging from the relevant broad-market index in the same window indicates
bonding specific to those tickers, not merely shared index-driven movement.
`</observation>`
<!-- src: belief/correlation-framework.md L137-143 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Index-baseline comparison against
SPY, QQQ, or IWM. `</observation>` `<observation>` A pair with no mutual
resemblance carries no sync signal regardless of index behavior — market
independence only qualifies a signal that is otherwise already present.
`</observation>` <!-- src: belief/market-independence.md L30 --> *(Note: this entry documents the market
phenomenon generically, including all three indices named in source. The
glossary's Market independence entry documents only the QQQ/SPY exchange-based
baseline actually used downstream — trader confirmed 2026-07-06 that later
trading-strategy and user-story content will use QQQ/SPY only, for practical
simplicity; no glossary change needed. IWM remains valid here as a general
market observation.)*
<!-- src: belief/correlation-framework.md L137-139 -->

**Scope caveat:** `<out-of-scope>` Does not imply group-specific bonding if
both tickers also resemble the relevant index over the same window — that
pattern is market-driven, not specific to the pair or group of tickers.
`</out-of-scope>`
<!-- src: belief/correlation-framework.md L138-139 -->

---

### MB-009 — Market Cap Effect on Sync Tightness

**Phenomenon:** `<observation>` Smaller-cap tickers under accumulation may
show tighter sync than larger-cap tickers, due to lower float relative to
buying interest. The same dollar amount of institutional buying produces a
more pronounced and consistent price/volume signature in a small-float
ticker than in a large-cap ticker. `</observation>`
<!-- src: belief/correlation-framework.md L150-154 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Tighter, more pronounced sync
signatures in small-float tickers under accumulation relative to large-cap
tickers experiencing comparable buying interest. `</observation>`
<!-- src: belief/correlation-framework.md L150-154 -->

**Scope caveat:** `<out-of-scope>` Does not imply a single detection
threshold or interpretation applies uniformly across market-cap tiers;
calibration by tier may be required. `</out-of-scope>`
<!-- src: belief/correlation-framework.md L153-154 -->

---

### MB-010 — Confluence: Independent Dimensions Activating Together

**Phenomenon:** `<observation>` Multiple genuinely independent observation
dimensions relating to the same theme may activate together. Four such
dimensions are recognized: bond cohesion and growth (see MB-001–006),
intraday setup density (MB-011), performance breadth (MB-012), and narrative
formation (MB-013). Each dimension is derivable from a domain or lens that
the others cannot explain away — they are orthogonal by construction.
`</observation>`
<!-- src: belief/correlation-framework.md L181-188 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Simultaneous activation of two or
more of the four confluence dimensions for the same theme, none of which
alone would be sufficient to establish the same read. `</observation>`
<!-- src: belief/correlation-framework.md L181-188 -->

**Scope caveat:** `<out-of-scope>` The dimensions are never combined into a
single score or weighted composite; no single observation, including bond
strength itself, is ever sufficient alone. `</out-of-scope>`
<!-- src: belief/correlation-framework.md L186-188 -->

*(set: confluence dimensions — see MB-011, MB-012, MB-013; first dimension,
bond cohesion and growth, is covered by MB-001–006, not a separate entry)*

---

### MB-011 — Intraday Setup Density

**Phenomenon:** `<observation>` A proportion of theme members may
simultaneously exhibit coiling or compression behavior on the intraday
timeframe. This is a distinct timeframe and pattern concept from daily-bar
sync, and can be active or inactive independent of it. `</observation>`
<!-- src: belief/correlation-framework.md L194-200 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Many members of one theme
coiling in parallel on the intraday timeframe, while other themes and the
broader market do not share that characteristic. `</observation>`
<!-- src: belief/correlation-framework.md L194-200 -->

**Scope caveat:** `<out-of-scope>` Does not indicate the direction of the
theme's next move; it is direction-neutral. `</out-of-scope>`
<!-- src: belief/correlation-framework.md L198-199 -->

*(member of set: confluence dimensions — see MB-010, MB-012, MB-013)*

---

### MB-012 — Performance Breadth

**Phenomenon:** `<observation>` The fraction of theme members participating
in the same directional move, and whether that fraction is expanding,
characterizes performance breadth — distinct from the theme's average
performance magnitude. `</observation>`
<!-- src: belief/correlation-framework.md L201-205 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` High breadth combined with low
dispersion across members indicates tickers moving together, consistent
with shared institutional interest. High breadth combined with high
dispersion indicates some members are driven while others lag.
`</observation>`
<!-- src: belief/correlation-framework.md L201-205 -->

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>`

*(member of set: confluence dimensions — see MB-010, MB-011, MB-013)*

---

### MB-013 — Narrative Formation

**Phenomenon:** `<observation>` A common storyline or topic may increasingly
surface across a group of tickers' company earnings reports, SEC filing or news coverage.
This is an entirely text-based signal, independent of price action in
either direction. `</observation>`
<!-- src: belief/correlation-framework.md L206-209 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied, 2026-07-06.)*
<!-- src: belief/correlation-framework.md L58-59 (origin anchor) -->

**Observable indicators:** `<observation>` Narrative convergence across a
group of tickers can appear before any behavioral sync threshold is crossed,
reversing the usual order in which bonding is observed first and a
connection is investigated second; sync may arrive later, or not at all.
Per-ticker narrative findings can also narrow or ground the search for what
holds a group of tickers together, independent of whether narrative
convergence itself first surfaced the group. `</observation>`
<!-- src: belief/correlation-framework.md L215-225; belief/filtering-logic.md L52-55 -->

**Scope caveat:** `<out-of-scope>` Does not indicate price direction — it is
independent of price action in either direction. `</out-of-scope>`
<!-- src: belief/correlation-framework.md L206-209 -->

*(member of set: confluence dimensions — see MB-010, MB-011, MB-012)*

---

### MB-014 — Ticker Multi-Theme Membership

**Phenomenon:** `<observation>` A single ticker can belong to more than one
theme at the same time, because it may form pair bonds with different sets
of tickers independently of each other. `</observation>`
<!-- src: belief/filtering-logic.md L61-62 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` The same ticker appearing as a
member of more than one bond cohort or theme concurrently, each via a
different pair-level bond. Tickers not yet assigned to any theme, but
showing active bonding signals, remain worth continued observation.
`</observation>`
<!-- src: belief/filtering-logic.md L61-64 -->

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>` *(trader-confirmed
2026-07-06.)*

---

### MB-015 — Theme Lifecycle (Overview)

**Phenomenon:** `<observation>` A theme's cohesion evolves through a
self-repeating lifecycle: Formation, Strengthening, Peak sync, Dissolution
(see MB-016–019). The lifecycle is not rigidly sequential in its
entry point — a theme can be triggered into any of these phases by any cause
(gradual accumulation, external shock, surprise event, or narrative
catalyst). `</observation>`
<!-- src: belief/filtering-logic.md L70-72 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` Each phase (MB-016–019)
carries its own distinct observable signature; which phase a theme currently
occupies is independently identifiable, not inferred from elapsed time or
from a fixed order of prior phases. `</observation>`
<!-- src: belief/filtering-logic.md L70-72 -->

**Scope caveat:** `<out-of-scope>` Does not imply the phases occur in a fixed
temporal sequence with a known trigger point — the lifecycle describes
recognizable states, not a predictable schedule. See MB-005: no lifecycle
phase indicates the timing of any specific price movement (e.g., a
breakout). Bonding/sync-rank development narrows which tickers the trader
monitors for chart-level setups; it provides no timing signal for those
setups, which are exploited independently (see trading-strategies.md).
`</out-of-scope>`

*(parent framing entry for set: theme lifecycle phases — see MB-016–019;
see Open items for the ID history behind this range)*

---

### MB-016 — Theme Lifecycle: Formation

**Phenomenon:** `<observation>` Theme formation typically begins with a
single pair bond — two tickers showing behavioral similarity during the same
period — not with a group appearing at once.  `</observation>` 
`<observation>` Formation can begin from narrative convergence across a group of tickers'
company narratives and news coverage, at the trader's discretion, even
before any sync threshold is crossed (see MB-013) — the reverse of the usual
sync-first path. `</observation>`
<!-- src: belief/filtering-logic.md L77-88 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` A single pair bond, with no
existing theme label, that has not yet accumulated additional bonded
members. `</observation>`
<!-- src: belief/filtering-logic.md L77-81 -->

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>` *(trader-confirmed
2026-07-06.)*

*(member 1 of 4, set: theme lifecycle phases — see MB-015, MB-017, MB-018, MB-019)*

---

### MB-017 — Theme Lifecycle: Strengthening

**Phenomenon:** `<observation>` Sync rank as the aggregate of its different
sync type inputs is gradually increasing across member tickers.
`</observation>`
<!-- src: belief/filtering-logic.md L91-93 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` This is the phase in which the
existence of the theme's underlying connection is confirmed as being a
market catalyst. `</observation>`
<!-- src: belief/filtering-logic.md L91-93 -->

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>` *(trader-confirmed
2026-07-06.)*

*(member 2 of 4, set: theme lifecycle phases — see MB-015, MB-016, MB-018, MB-019)*

---

### MB-018 — Theme Lifecycle: Peak Sync

**Phenomenon:** `<observation>` The aggregated sync rank of the theme member
tickers is reaching a local high (time-wise). `</observation>`
<!-- src: belief/filtering-logic.md L96-99 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` This is the phase in which it is
appearing obvious that the underlying connection between the tickers is a
market catalyst based on which large market participants are buying and
selling a theme rather than individual tickers (no stock picking). `</observation>`
<!-- src: belief/filtering-logic.md L98-101 -->

**Scope caveat:** `<out-of-scope>` See MB-005: has no bearing on chart-level
setups and may or may not be accompanied by chart constellations with a
higher probability of imminent price moves. `</out-of-scope>`
<!-- src: belief/filtering-logic.md L100-101 -->

*(member 3 of 4, set: theme lifecycle phases — see MB-015, MB-016, MB-017, MB-019)*

---

### MB-019 — Theme Lifecycle: Dissolution

**Phenomenon:** `<observation>` Members are in the phase of decoupling in terms of 
aggregated sync rank decrease.
`</observation>`
<!-- src: belief/filtering-logic.md L108-109 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` Aggregated sync rank is gradually
falling and nearing a local low, as the underlying theme connection is not
acting as a market catalyst anymore. `</observation>`
<!-- src: belief/filtering-logic.md L108-111 -->

**Scope caveat:** `<out-of-scope>` See MB-020: this does not imply the theme
ceases to exist — the connection may simply not be in play, and that could
change at any point in time; a theme only stops existing if its underlying
connection is no longer valid. See MB-005: has no bearing on chart-level
setups and may or may not be accompanied by chart constellations with a
higher probability of imminent price moves. `</out-of-scope>`
<!-- src: belief/filtering-logic.md L108-111 -->

*(member 4 of 4, set: theme lifecycle phases — see MB-015, MB-016, MB-017, MB-018)*

---

### MB-020 — Theme Validity Persists While Its Connection Remains Valid

**Phenomenon:** `<observation>` A theme continues to exist for as long as its
underlying connection remains valid, independent of momentary sync-rank
strength. A connection can go through periods where it produces no
observable sync (no shared catalyst active) without the connection itself
having broken down. `</observation>`
<!-- trader-supplied original content, 2026-07-06 — not sourced from any
belief/ snapshot file; the source material does not distinguish theme
validity from momentary sync-rank strength, which this entry corrects. -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` A theme's members can show low or
absent sync rank for extended periods without the trader treating the
theme's connection as invalidated — sync rank fluctuation alone is not
evidence the connection no longer holds. `</observation>`

**Scope caveat:** `<out-of-scope>` None `</out-of-scope>` *(trader-confirmed
2026-07-06.)*

**Example:** `<example>` A connection may be that a set of tickers share the
same sub-provider. At times a catalyst related to that sub-provider (e.g. a
supply shortage) drives synchronized movement across the tickers. At other
times, with no such catalyst active, the same tickers show no elevated sync
— but the connection itself remains valid throughout; it has not stopped
being true that they share the sub-provider. `</example>`
<!-- trader-supplied original content, 2026-07-06 -->

*(relates to MB-007 — connection is the theme-forming requirement alongside
a pair bond; this entry clarifies the connection's persistence is
independent of ongoing sync-rank strength)*

---

### MB-021 — Structural Leadership Within a Confirmed Theme

**Phenomenon:** `<observation>` A confirmed theme has a structural-leadership
dimension, separate from conviction: individual tickers can persistently
lead or lag the rest of the theme's performance. This is a standing
structural property of the theme, not a one-time observation.
`</observation>`
<!-- src: belief/correlation-framework.md L227-231 -->

**Conditions:** `<observation>` Market-condition agnostic: equally
informative during selling periods and buying periods. `</observation>`
*(trader-supplied default, per established corpus convention — see Open
items.)*

**Observable indicators:** `<observation>` One or a small number of tickers
within a theme persistently lead or lag the rest of the theme's performance
across time, not just within a single move. `</observation>`
<!-- src: belief/correlation-framework.md L227-231 -->

**Scope caveat:** `<out-of-scope>` Does not imply which specific ticker will
lead is knowable in advance from bonding data alone. Only the phenomenon
(leadership is a standing structural property) is captured here; no
exploitation logic (STR) or capability (US) is authored from it yet, pending
further trader input on identifying and exploiting leadership (before or
during consolidation, rotation criteria, best-ticker selection).
`</out-of-scope>`
<!-- src: belief/correlation-framework.md L230-231 -->

---

## Open items

- MB-001, MB-002, MB-005–021 (i.e. every current entry) Conditions fields
  are trader-supplied (2026-07-06), not traced to their own section's
  source text — flagged inline per Rule 11 provenance discipline; their only
  real anchor is Type 3's own Conditions statement (L58-59). This
  "market-condition agnostic" default, originally supplied by the trader for
  correlation-framework.md entries only, has now been extended across all
  entries derived from every belief/ file processed to date; trader has not
  objected to this extension when raised.
- MB-001, MB-002, MB-003, MB-012, MB-014, MB-016, MB-017, MB-020 Scope
  caveats are trader-confirmed "None" (state (b) per
  market-behavior-authoring.md v0.4) — handoff-ready with respect to this
  field.
- ID history (renumbered 2026-07-06): two entries were drafted, then removed
  outright, during this pass — the original "Theme Lifecycle: Breakout and
  Dispersion" (drafted as MB-019, retired: a breakout is a chart-level
  event, not a theme-lifecycle stage — the source material's implicit
  price-timing/lifecycle-stage link is a misconception; MB-015's Scope
  caveat carries the corrected relationship) and "Screening-Based Blind
  Spot" (drafted as MB-021, removed: describes trader/screening practice,
  not market behavior — converted into trading-strategies.md STR-010). The
  three entries then numbered MB-020/022/023 were renumbered down to
  MB-019/020/021 to close the resulting gaps, per trader instruction — a
  deliberate one-off exception to market-behavior-authoring.md's normal
  "IDs never reused" rule, made while this document is still in progress
  (pre-handoff) and not yet cited by external references outside this
  corpus. Current mapping: MB-019 = Theme Lifecycle: Dissolution (was
  MB-020), MB-020 = Theme Validity Persists While Its Connection Remains
  Valid (was MB-022), MB-021 = Structural Leadership Within a Confirmed
  Theme (was MB-023). trading-strategies.md's STR-009 citation of MB-015 is
  unaffected (MB-015 itself did not renumber); no other cross-doc citations
  referenced MB-020/022/023 before this renumbering.
- Resolved: the "Structural leadership" aside (source §2.9,
  correlation-framework.md L227-231) was pulled directly into MB-021
  (formerly MB-023) per trader instruction (2026-07-06). MB-021 captures
  only the phenomenon; the leadership-identification/exploitation logic
  (STR/US) remains genuinely deferred pending further trader input, since no
  trigger-condition content exists in any current source for it.

## Change log

- v0.7 (2026-07-06) — elevated and broadened MB-005 into the corpus's
  canonical statement of sync/theme-development-independent-of-price-timing:
  retitled from "Bonding Strength and Future Price Movement (Uncertain
  Relationship)" to "Sync and Theme Development Is Independent of
  Price-Movement Timing"; Phenomenon/Observable indicators/Scope caveat
  broadened to cover sync rank and lifecycle stage generally, not only
  bonding strength (consolidating already-sourced content from
  correlation-framework.md L98-102, previously only cited in MB-006's own
  caveat). Position unchanged (slot 5, immediately after the foundational
  MB-001–004 sync-type entries) — already the earliest point the principle
  can meaningfully sit. MB-006, MB-015, MB-018, MB-019 Scope caveats trimmed
  to cross-reference MB-005 instead of restating it; MB-019's caveat also
  trimmed to cross-reference MB-020 for its separate theme-persistence
  point, removing a second duplication found in passing. STR-001 in
  trading-strategies.md updated for MB-005's new title.
- v0.6 (2026-07-06) — trader reworked MB-018 (Peak Sync) and MB-019/former-
  MB-020 (Dissolution) content directly, resolving the two flagged
  duplications (MB-018 vs. MB-015, and MB-020 vs. MB-022) — no residual
  action needed there. Trader also instructed a numbering correction: the
  gaps left by the two removed entries (former MB-019, former MB-021) were
  closed by renumbering MB-020→MB-019, MB-022→MB-020, MB-023→MB-021, with
  all cross-references updated throughout this document. This is a
  deliberate, one-off exception to the "IDs never reused" rule while the
  document is still pre-handoff — see Open items for the full ID-history
  note and mapping.
- v0.5 (2026-07-06) — cleanup pass: fixed typos introduced by manual edits
  (MB-017 "gardually"→"gradually"; MB-018 "synk rank"→"sync rank", "should
  monitored"→"should be monitored"; MB-020 "and and"→"and", capitalization).
  Corrected a stale Open items cross-reference range ("MB-005–021") that
  still implied MB-021 exists; it was removed in v0.4. Two duplications
  flagged for trader decision, not yet changed — see standalone note.
- v0.4 (2026-07-06) — trader review of manual edits + further corrections:
  MB-019 tombstone entry removed entirely from the document (no value
  keeping a retired stub in the body; ID-skip recorded in Open items only).
  MB-021 (Screening-Based Blind Spot) removed from this document — trader
  determined it describes trader/screening practice, not market behavior;
  converted into a new trading-strategies.md entry. MB-023's Scope caveat
  reworded to remove the direct `timing-interpretation.md` filename
  reference (a backward link to snapshot source material does not belong in
  handoff-ready deliverable content); phenomenon and remaining caveat content
  unchanged. Trader also manually edited MB-017, MB-018, MB-020 to remove
  chart-language mixing from their Phenomenon fields; review found 3
  Observable-indicators/Phenomenon fields the manual pass did not yet reach
  (MB-017, MB-018, MB-020) — flagged in Open items with proposed fixes,
  not applied pending trader confirmation.
- v0.3 (2026-07-06) — trader-directed corrections following review: MB-014,
  MB-016, MB-017 Scope caveats confirmed "None." MB-019 ("Theme Lifecycle:
  Breakout and Dispersion") retired without replacement — trader identified
  a fundamental misconception in the source material linking specific price
  movements (breakout) to theme-lifecycle stage; any MB/STR/US content built
  on that link is invalid. MB-015's Scope caveat rewritten with the
  corrected relationship (sync/theme development narrows monitoring scope
  only, no setup-timing signal) and MB-018's Scope caveat cross-references
  it. New MB-022 (Theme Validity Persists While Its Connection Remains
  Valid) — trader-supplied original content, not sourced from any snapshot
  file, correcting a gap in the source's framing (sync-rank fluctuation ≠
  connection invalidation). New MB-023 (Structural Leadership Within a
  Confirmed Theme) — pulled directly from correlation-framework.md L227-231
  per trader instruction, since the deferral target (`timing-interpretation.md`)
  proved to be an unpopulated placeholder; only the phenomenon is captured,
  exploitation logic remains genuinely deferred (no source content exists
  for it yet).
- v0.2 (2026-07-06) — belief/ remaining-files routing+authoring pass
  (filtering-logic.md, market-independence.md, timing-interpretation.md).
  Expanded MB-007 (minimum-seed nuance), MB-008 (no-resemblance observable
  indicator), MB-013 (added filtering-logic.md source anchor). New entries
  MB-014 (Ticker Multi-Theme Membership), MB-015–020 (Theme Lifecycle
  overview + 5-member phase set), MB-021 (Screening-Based Blind Spot). 4 new
  Scope caveats opened as report-backs (MB-014, MB-016, MB-017, MB-019).
- v0.1 (2026-07-06) — initial draft: 13 entries (MB-001–013) authored from
  `snapshot-routing.md` (correlation-framework.md), per
  market-behavior-authoring v0.5 and authoring-hygiene v0.10.
