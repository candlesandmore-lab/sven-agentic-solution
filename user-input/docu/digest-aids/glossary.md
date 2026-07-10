# Glossary — Agent-Build-Agents Input Corpus
v0.8 — 2026-07-06

<scope>
Authoritative terminology for the four input documents and their digest aids.
If any deliverable doc contradicts this glossary, the doc is wrong. Every
specialized noun used in any deliverable must have an entry here.

Rule: before introducing a new specialized term in a deliverable, add its
glossary entry (definition + anti-synonyms + status). No exceptions.
</scope>

## How to read entries

Each entry has:
- **Definition** — precise meaning as used in this corpus
- **Anti-synonyms** — terms this must not be confused or interchanged with
- **Status** — `standard`, `banlisted`, `tech-restricted`, `common`, or `placeholder`
- **Notes** — optional; usage guidance, worked examples, rationale

## Roles (see roles.md for full detail)

### Human trader
<definition>The single human domain expert whose knowledge and requirements drive the corpus.</definition>
Anti-synonyms: `trader` (bare), `user`, `operator`, `client`
Status: standard
Note: The bare word "trader" is prohibited. Always qualified as "human trader".

### Technical Trader Solution
<definition>The complete delivered artifact — the union of interface, data integrations, deterministic components, and any internal AI-based components the client project chooses to include.</definition>
Anti-synonyms: `cockpit system` (retired name), `cockpit` (bare), `system` (bare), `app`, `tool`, `platform`, `product`
Status: standard
Note: Always use the full three-word form "Technical Trader Solution". Bare "Solution", partial forms "Technical Trader" and "Trader Solution", and the retired name "cockpit system" (and bare "cockpit") are all prohibited where this role is meant. File-path and identifier references excluded.

## Technology terms — tech-restricted

<rule strictness="hard">
The following terms describe technology internal to the Technical Trader Solution's
boundary. They may appear in (a) the tech-stack constraints doc and (b)
non-functional requirements within user stories. They must not appear in
market-behavior content, trading-strategy content, or user-story functional
content.
</rule>

### Agent
<definition>An AI-based component with tool use and orchestration.</definition>
Status: tech-restricted
Note: Implementation choice, not a role. Prohibited in market-behavior, trading-strategy, and user-story functional content.

### LLM
Status: tech-restricted
Note: Implementation choice. Same prohibition as `agent`.

### AI
Status: tech-restricted
Note: Same prohibition. Refer to capability desired, not the technology used.

### API, database, service, framework
Status: tech-restricted
Note: Additional tech terms are tech-restricted by default even if not listed here. When in doubt, ask.

### ADR (Average Daily Range)
<definition>A measure of a ticker's typical intraday price movement expressed as a percentage of price. Used as a universe screening filter (minimum threshold: ADR > 3.5%) and as a normalization factor for group performance comparisons across tickers with different price levels and volatility profiles.</definition>
Status: tech-restricted
Replacement for deliverable docs: "volatility" in market-behavior and trading-strategy content. User stories may cite the ADR threshold in non-functional requirements.

### wld (window length in days)
<definition>Implementation abbreviation for the lookback window parameter used in chart encoding and pairwise similarity computation. Three values used: 14 days, 21 days, 35 days.</definition>
Status: tech-restricted
Replacement for deliverable docs: "rolling window length" in strategy and user-story functional content. User stories may cite the three window-length values in non-functional requirements.

## Loaded terms — banlist (strict-sense only)

The following terms have precise mathematical, statistical, or ML meanings and
have historically been used loosely in parent-project source material. In this
corpus they may appear only in their strict sense, wrapped in a `<strict-term>`
marker with an accompanying definition or citation.

### Correlation
<definition>Statistical correlation in the strict sense (Pearson, Spearman, or explicitly named variant) with numeric context. Not "things that move together in a way that suggests a connection".</definition>
Status: banlisted (strict sense only)
Replacement for loose usage: "co-movement", "fact-based intuition", "observed tendency to move together", or a description of the specific observable indicator.
Worked example:
- Bad: "There is a correlation between rising oil prices and airline stock declines."
- Good: `<observation>` Airline stock prices have shown an observed tendency to decline in the days following material rises in crude oil prices. `</observation>`

### Causation
Status: banlisted (strict sense only)
Replacement: "leads to", "precedes", "is followed by", "coincides with" — chosen for the actual claimed relationship.

### Significance
Status: banlisted (strict sense only)
Replacement: "notable", "material", "large enough to act on" — non-statistical significance.

### Model
Status: banlisted (strict sense only); tech-restricted when the ML meaning is intended.
Replacement for informal use: "framework", "description", "mental model" — with a qualifier making the informal sense explicit.

### Signal
Status: banlisted (strict sense only)
Replacement: "indicator", "trigger", "condition", "observation" — chosen for the actual meaning.

### Pattern
Status: banlisted (strict sense only)
Replacement: "recurring configuration", "observed shape", "typical sequence" — chosen for the actual meaning.

## Domain terms — standard

### Theme
<definition>A trader-approved collection of tickers sharing a confirmed connection — grounded in concrete company-level facts — that may explain why institutional money buys or sells them together. Requires both observed behavioral sync and a confirmed connection; either alone is insufficient. A theme has a self-repeating lifecycle (formation, strengthening, peak sync, breakout, dissolution) and its membership is defined by observed co-movement and trader judgment, not by classification systems.</definition>
Anti-synonyms: `candidate net`, `group` (bare — see Common terms), `sector`, `topic`, `watchlist`
Status: standard
Note: Two sub-types exist — curated theme (manually maintained, durable) and dynamic theme (behaviorally surfaced, sync-rank driven lifecycle). Emergent theme = a dynamic theme being observed for the first time. The Technical Trader Solution treats all themes as a single unified concept; the sub-type distinction exists in trader belief and authoring.

### Candidate net
<definition>The largest connected component of tickers whose pairwise similarity scores newly crossed the detection threshold in a given nightly batch run. A candidate net is the automated surface — an invitation to investigate — never a theme. Trader confirmation of a meaningful connection is required to convert it into a theme. Multiple candidate nets may be surfaced per batch run and may be ordered by aggregate bond strength.</definition>
Anti-synonyms: `theme`, `group`, `watchlist`, `universe`, `cluster`
Status: standard

### Sync
<definition>Observable behavioral co-movement between two or more tickers during the same period, regardless of the existence of a shared cause. Manifests in three independent signal types: Type 1 (spike co-activation), Type 2 (momentum density with resemblance), Type 3 (structural resemblance). Sync is a necessary but not sufficient condition for theme conviction — a confirmed connection is also required.</definition>
Anti-synonyms: `correlation` (strict statistical sense — banlisted), `co-movement` (weaker: does not carry the full depth of the sync concept), `resemblance` (structural resemblance is one type of sync, not the whole)
Status: standard

### Sync rank
<definition>A measure of ongoing cohesion strength between two or more tickers: how tightly bonded they are to each other over a sustained period. Driven by all three sync types. Applied at two levels: (a) pairwise — the strength of the bond between two specific tickers; (b) aggregate — the cohesion of a candidate net or theme across all its members. Not a price-move predictor — high sync rank indicates the tickers are currently moving closely together; it says nothing about timing or direction of any subsequent move. Sync rank decays over time rather than accumulating indefinitely; historical sync occurrences lose influence.</definition>
Anti-synonyms: `score` (generic), `rating`, `price-move signal`, `momentum indicator`
Status: standard
Note: "Bonding strength" is a synonym for sync rank; both terms are correct. The canonical form is "sync rank." See also bonding strength.
Note: The trajectory of sync rank (increasing, decreasing, steady) carries informational weight; absolute persistence of a rank value does not.

### Bonding strength
<definition>Synonym for sync rank. The aggregate form of sync rank as used specifically in the scatter view (Y-axis) and theme maintenance contexts. See sync rank for the full definition.</definition>
Anti-synonyms: `performance`, `momentum`
Status: standard
Note: "Sync rank" is the canonical term. "Bonding strength" is retained as an established label for the theme-level aggregate context; both terms are interchangeable.

### Bond cohort
<definition>A set of tickers connected transitively through pairwise bonds — if pair A–B is bonded, pair B–C is bonded, and pair A–C is bonded, then {A, B, C} form one bond cohort. Membership is purely structural, derived only from which pairs are bonded, independent of detection timing or trader judgment. A bond cohort may or may not later be surfaced as a candidate net (a trader solution-level artifact — see candidate net) and may or may not later be confirmed as a theme (requires an accepted connection).</definition>
Anti-synonyms: `candidate net` (a solution-level artifact, not a raw structural fact), `theme` (requires a confirmed connection), `bond network` (the full computational state across all eligible tickers, not one connected subset), `group` (bare, no specialized meaning), `cluster`
Status: standard

### Pair bond
<definition>The sync rank of a specific pair of tickers. Theoretically every pair of tickers has a pair bond; what varies is the sync rank value. A pair bond is considered active when the sync rank crosses the detection threshold, indicating evidence of a non-random connection between those tickers.</definition>
Anti-synonyms: `theme` (a theme requires trader approval and a connection; a pair bond is behavioral evidence), `connection` (the connection is the explanatory link; the pair bond is the behavioral evidence)
Status: standard

### Bond / Bonding
<definition>The state of accumulated pairwise sync evidence between two tickers across signal types and time. "Bonding" is the process, usually indicating an increasing sync rank. There is always a bond between any two tickers; what differs is the sync rank value or, for groups of tickers, the aggregated sync rank. Used at two levels: (a) pairwise — the bond between two specific tickers; (b) theme-level — how strongly theme members bond with each other in aggregate (bonding strength / sync rank).</definition>
Anti-synonyms: `correlation` (strict), `pairing`, `linking`
Status: standard

### Bond network
<definition>The complete living state of all pairwise sync ranks across eligible tickers at a given point in time. A computational artifact recalculated nightly. Explicitly distinct from any theme — the bond network is the raw material from which candidate nets emerge and from which any pair's or group of tickers' aggregated sync rank can be computed. It is the source of truth and maintains historical values.</definition>
Anti-synonyms: `theme`, `group` (bare), `graph` (a graph visualization can represent the bond network but is not the bond network itself), `watchlist`
Status: standard
Note: The distinction between the bond network and a theme is a hard constraint (CUS P1). The bond network is a computational artifact; a theme is a trader judgment.

### Connection
<definition>The explanatory link — grounded in concrete company-level facts — that could justify why institutional money would buy or sell a set of tickers together. A connection is required alongside observed behavioral sync to convert a candidate net into a theme. It does not need to be known before detection; it is confirmed or hypothesized after the behavioral signal is observed. Connections establish an additional dimension to static GICS sectors and industries — they are not substitutes for sector classification but explanations of specific shared institutional interest.</definition>
Anti-synonyms: `narrative formation` (narrative formation is one input to finding a connection, not the connection itself), `hypothesis` (a hypothesis is a candidate connection before confirmation), `category`, `sector`, `label`
Status: standard
Note: A connection is valid when concrete company-level facts — what each company makes or does, who it serves, what is currently happening to it — tell a coherent story of specific shared institutional interest. Directional (explains why those particular tickers), not categorical (mere industry-tag membership). The qualified forms "confirmed connection" (trader-accepted) and "hypothesized connection" (under investigation) are both valid in deliverables.
Worked example:
- Good: a set of tickers that all specialize in one narrow shared activity (e.g. one specific component type for one specific end-use buildout) can be a valid connection even though they also all sit within one broader industry classification.
- Bad: tickers sharing only a broad industry-tag membership, with no narrower shared-activity story underneath, do not have a connection — the tag alone never establishes one, regardless of how narrow or unusual the tag is.
<!-- src: belief/filtering-logic.md L32-42 -->

### Mover order (first / second / third mover)
<definition>The sequential position of a ticker among those breaking out of a synchronized theme consolidation, ordered by when each ticker's individual break is confirmed. First mover: the ticker that leads the group out of consolidation — highest reward, highest relative risk, since no other member's break yet confirms the theme is activating. Second mover, third mover: each subsequent confirmed break carries lower risk and lower reward than the one before it, because the prior break(s) already confirm activation; which later movers a trader still acts on depends on overall market conditions.</definition>
Anti-synonyms: `structural leadership` (a standing, ongoing property of a confirmed theme — which ticker(s) persistently lead or lag the theme's performance over time; mover order instead describes confirmed *post-break* sequencing for one specific breakout event), `leadership` (a distinct, not-yet-authored corpus topic — identifying which ticker will lead *before or during* consolidation, and rotation criteria; reserved for `timing-interpretation.md`, unpopulated as of this corpus's snapshot), `rank`, `score`
Status: standard
Note: Risk decreases and conviction increases with each subsequent mover, since every earlier confirmed break is itself evidence the theme is genuinely activating.
<!-- src: belief/filtering-logic.md L127-136 -->

### Structural leadership
<definition>A standing, ongoing property of a confirmed theme, separate from conviction: one or a small number of tickers persistently lead or lag the rest of the theme's performance over time, not just within a single move.</definition>
Anti-synonyms: `mover order` (a one-time, per-breakout sequencing of confirmed entries, not an ongoing structural property), `leadership` (the not-yet-authored corpus topic of identifying/exploiting which ticker leads — reserved for `timing-interpretation.md`; this entry captures only that the property exists, not how to identify or act on it), `conviction`
Status: standard
Note: Which specific ticker leads is not knowable from bonding data alone per this entry — identification and exploitation logic are reserved for a future belief-interview session (`timing-interpretation.md`, unpopulated as of the 2026-07-02 snapshot).
<!-- src: belief/correlation-framework.md L227-231 -->

### Structural resemblance
<definition>The Type 3 sync signal — visual similarity between two tickers' chart shapes during the same or adjacent periods: similar shape, rhythm, and timing of pauses and pushes, regardless of absolute price magnitude. Assessed pairwise. Market-condition agnostic — resemblance during selling periods carries the same informational weight as during buying periods.</definition>
Anti-synonyms: `correlation` (strict statistical sense), `similarity score` (a computed score may measure structural resemblance but is not the same concept), `co-movement` (implies directionality; structural resemblance does not require same direction), `resemblance` (bare — "structural resemblance" is the required form in this corpus)
Status: standard
Note: "Resemblance" alone carries the same meaning informally but "structural resemblance" is the required qualified form in deliverables.

### Curated theme
<definition>A theme manually maintained by the human trader over time, anchored to a durable connection reflecting accumulated knowledge of market structure (e.g. nuclear energy stocks, established biotech sub-groupings). Curated themes are existing themes in the existing database, maintained manually. Contrasted with dynamic themes, which are behaviorally surfaced and have a sync-rank driven lifecycle. Both types share the same object definition and infrastructure. Conceptually, curated themes may in the future be fully replaced by dynamic themes.</definition>
Anti-synonyms: `dynamic theme`, `emergent theme`, `auto-detected theme`
Status: standard

### Dynamic theme
<definition>A theme that is behaviorally surfaced — detected from observed increasing sync among tickers — and has a sync-rank driven lifecycle (formation, strengthening, peak sync, breakout, dissolution). Contrasted with curated themes, which are manually maintained. Emergent themes are a subset: dynamic themes being observed for the first time. Both curated and dynamic themes share the same object definition and infrastructure.</definition>
Anti-synonyms: `curated theme`, `sector group`, `screener result`
Status: standard
Note: "Dynamic theme" is the canonical term for non-curated themes in this corpus. Source docs also use "emergent theme" for the same concept (CF §2.8); "dynamic theme" is the canonical form in deliverables. "Emergent theme" refers specifically to the first-detection state of a dynamic theme.

### Emergent theme
<definition>A theme surfaced from currently observed, increasing behavioral bonding among tickers that may not share an obvious or pre-existing label. Emergent themes are dynamic themes being observed for the first time (= emerging). They provide the early-stage detection edge that morning screeners structurally miss.</definition>
Anti-synonyms: `curated theme`, `sector group`, `screener result`, `dynamic theme` (dynamic theme is the persistent state; emergent theme is the first-detection point)
Status: standard
Note: Every emergent theme becomes a dynamic theme. Not every dynamic theme is still emergent.

### Market independence
<definition>The property of a pair sync signal that holds when two tickers show mutual resemblance while simultaneously diverging from the relevant broad-market index in the same window. A market-independent sync signal is high-value because it indicates group-specific institutional activity rather than index beta. A pair that resembles both each other and the index produces a low-value, index-explained signal. Market independence is not a separate analytical step — it is assessed as part of the same observation as the sync signal itself.</definition>
Anti-synonyms: `beta signal` (the index-driven counterpart), `index co-movement`, `sector-wide drift`
Status: standard
Note: Index baseline by listing exchange: QQQ for NASDAQ-listed names, SPY for all others. Divergence threshold is a qualitative judgment; no generic level is defined — resolution is delegated to user stories as an acceptance criterion.

### Type 1 (spike co-activation)
<definition>A sync signal in which two or more tickers show sharp price/volume spikes within ±2–3 days of each other in the same direction. Contributes to sync rank alongside Type 2 and Type 3 signals.</definition>
Anti-synonyms: `phase`, `stage`, `level` (Type 1/2/3 are independent signal types, not a sequence)
Status: standard
Note: See also Type 2, Type 3. The three sync types are independent expressions of bonding and can co-occur.

### Type 2 (momentum density with resemblance)
<definition>A sync signal characterized by sustained directional momentum with elevated volume over multiple weeks ("volume density"), manifesting as pairwise structural resemblance within a larger group. The higher-energy, directional version of Type 3; inherently includes the resemblance component.</definition>
Anti-synonyms: `phase`, `stage`, `level`
Status: standard
Note: See also Type 1, Type 3.

### Type 3 (structural resemblance)
<definition>A sync signal in which two tickers show visually similar chart structure during the same or adjacent periods — similar shape, rhythm, timing of pauses and pushes — regardless of price magnitude or direction. Market-condition agnostic; temporary and pairwise.</definition>
Anti-synonyms: `phase`, `stage`, `level`
Status: standard
Note: See also Type 1, Type 2. See structural resemblance for the full characterization of the visual similarity criterion.

### Conviction
<definition>The human trader's mental readiness to act on a theme — committing attention, watchlist placement, and ultimately trade consideration — and also describes the strength of belief that a theme exists (pre-trading decision). Conviction requires both observed behavioral sync and a confirmed connection; neither alone is sufficient. Conviction is modulated by sync rank (a higher sync rank lowers the setup quality bar required to enter) and increased by confluence of multiple independent observation dimensions. Conviction is never a computed score — it is a trader judgment.</definition>
Anti-synonyms: `confidence score`, `probability`, `rank`, `rating`
Status: standard

### Setup
<definition>A chart configuration that, in the human trader's judgment, offers a defined trade entry opportunity — characterized by specific structural conditions such as a tightening range, flag formation, base, or ledge. A setup is always assessed by trader eyes and never automated. Setup quality is a prerequisite for entry; sync rank modulates how high the setup quality bar must be, but does not replace it.</definition>
Anti-synonyms: `signal` (a signal may indicate that a setup is forming; a setup is the assessed chart configuration), `trigger` (the trigger is the break, not the setup itself), `pattern` (strict banlisted sense)
Status: standard
Note: "Setup" in this corpus refers exclusively to the chart-structure opportunity; it must never be interpreted as system configuration or preparation.

### Confluence
<definition>The state in which multiple genuinely independent observation dimensions — bond cohesion, intraday setup density, performance breadth, narrative formation — activate together for the same group of tickers (candidate net or theme). Confluence is the overlay of observations in multiple dimensions at the same time; it increases the human trader's conviction that the theme may be approaching an active move, beyond what any single dimension signals. The dimensions are never combined into a single score or weighted composite — the human trader reads the combination and decides.</definition>
Anti-synonyms: `composite score`, `weighted average`, `combined signal`, `aggregate metric`, `convergence` (related but not equivalent — convergence may refer to price-level convergence or other narrower concepts)
Status: standard

### Performance breadth
<definition>The fraction of theme members participating in the same directional move, and whether that fraction is expanding. Assessed in combination with dispersion: high breadth + low dispersion signals shared institutional interest; high breadth + high dispersion signals some members driven while others drag. Performance breadth measures the expanding fraction, not the average performance magnitude. One of four confluence dimensions.</definition>
Anti-synonyms: `breadth` (a generic market term expressing the advance/decline ratio of a broad market index; performance breadth is specifically the fraction of theme members participating in the same direction), `average performance`, `group return`, `momentum`
Status: standard

### Performance dispersion
<definition>A measure of the difference in price performance between theme member tickers over a specified timeframe.</definition>
Anti-synonyms: `sync rank` (measures cohesion of movement, not performance difference), `performance breadth` (measures the fraction participating in the same direction, not the magnitude of their differences), `volatility`
Status: standard

### Intraday setup density
<definition>The proportion of theme members simultaneously exhibiting coiling or compression behavior on the intraday timeframe, independent of daily-bar sync. A high intraday setup density — relative to other themes and the broader market — is read as a sign of institutional positioning. Direction-neutral: it increases alertness without predicting move direction. One of four confluence dimensions.</definition>
Anti-synonyms: `density` (too broad and generic), `volatility`, `compression level`, `setup count` (intraday setup density is a proportion across members, not a count or a volatility measure)
Status: standard

### Narrative formation
<definition>A common storyline or topic increasingly surfacing across a group of tickers' company narratives and news coverage — a text-based signal entirely independent of price action. Functions in two ways: (a) as the fourth confluence dimension for already-confirmed themes (corroborating that a theme is approaching an active move); (b) as an alternative theme-genesis path — narrative convergence can constitute a connection between the associated tickers and lead theme formation before any sync threshold has been crossed, at the human trader's discretion. Per-ticker narrative findings also serve as input to connection investigation generally.</definition>
Anti-synonyms: `sentiment` (sentiment is directional — positive/negative; narrative formation is about topic convergence, not sentiment), `news` (news is the raw input; narrative formation is the pattern of convergence across tickers)
Status: standard

### Eligible universe
<definition>The set of tickers that currently meet the human trader's screening filters (volatility, price relative to moving average, rank percentile, volume history) and are included in nightly batch encoding and pairwise computation. Theme members that fall below universe filters are tracked but not removed automatically — they remain in encoding and pairwise computation. "Universe" alone is used interchangeably.</definition>
Anti-synonyms: `watchlist` (a watchlist is a subset or output; the eligible universe is the full eligible set), `theme` (a theme is a trader-approved subset of the eligible universe)
Status: standard

## Common terms (not specialized)

<rule strictness="hard">
Terms in this section carry no specialized domain meaning in this corpus. They
are listed to prevent re-flagging in future vocabulary gate scans. They must not
be used in deliverables where a domain term applies. When a passage needs to
refer to a collection of tickers, use the most specific applicable domain term
(theme, candidate net, bond network, eligible universe).
</rule>

<rule strictness="hard">
If a passage uses a common-status term in a way that no domain term's
anti-synonyms confirm is safe to replace with plain English, this is not a
silent-substitution case — see authoring-hygiene Rule 8 (common-status term
ambiguity stop).
</rule>

### Group
Status: common
Note: In this corpus "group" carries no specialized domain meaning beyond its ordinary English sense (a collection of tickers without further bearing). Must not be used where `theme`, `candidate net`, `bond network`, or `eligible universe` is intended. Source docs use "group" and "theme" interchangeably in some passages (e.g. FL:L13); this usage is not carried into deliverables. Usage convention: always write "group of tickers" in full when this generic sense is meant — never bare "group" alone — so the generic sense reads as visually distinct from a domain-term slip. Confirmed by trader clarification CLARIF-001 (2026-07-06, correlation-framework.md §2.1–2.2 usages).

### Tag
Status: common (retired term)
Note: Historical label for trader-created themes in SARMOCONIA prior to the single-theme-concept decision (CUS P3, Session 41). No active domain meaning in the current corpus. Use `theme` in deliverables.

### Scheme
Status: common
Note: Does not bear any specialized meaning in this corpus. Not to be used in deliverables.

### Category
Status: common
Note: Used only in its ordinary English sense (broad grouping by shared attribute), as a counterexample to what a valid connection is not. No specialized domain definition. Must not be confused with `connection`.

## Growth rule

<rule strictness="hard">
Any specialized noun used in any deliverable doc must have a glossary entry
before it appears. Adding a term to a doc without adding its glossary entry
is a rubric failure.

When an authoring skill needs to use subject-matter language and the required
term is absent from this glossary, the skill must either:
(a) fall back to the nearest confirmed glossary term that accurately covers
    the concept — using the anti-synonyms and related entries as a guide; or
(b) stop and request human trader clarification before continuing.

Guessing or inventing definitions is not permitted. If the skill is uncertain
whether an existing glossary entry covers the needed concept, it must ask
rather than assume.
</rule>

## Change log

- v0.9 (2026-07-07) — trader-peer review session corrections: Type 1 (spike
  co-activation) definition reworded — dropped "primary for pair
  activation" (legacy term, incorrectly implied primacy), now states it
  contributes to sync rank alongside Type 2/3; Sync rank definition extended
  with decay-over-time framing, new Note added on trajectory (direction of
  change) carrying informational weight over absolute persistence; new
  standard entry Performance dispersion added (distinct from Performance
  breadth and Sync rank — required before trading-strategies.md STR-003
  could be cleanly edited to stop conflating dispersion with cohesion).
- v0.8 (2026-07-06) — added Worked example to the Connection entry (optical-
  components/Uranium-tag directionality illustration, from
  `belief/filtering-logic.md` §1.1); added new standard entries Mover order
  (first/second/third mover — confirmed post-break entry sequencing) and
  Structural leadership (standing per-theme lead/lag property, pulled
  directly from correlation-framework.md L227-231 per trader instruction
  since its original deferral target, `timing-interpretation.md`, proved
  empty). Both distinguished from each other and from the still-unauthored
  pre-break "leadership identification" topic deferred to
  `timing-interpretation.md`. Driven by the belief/ remaining-files
  routing+authoring pass (filtering-logic.md, market-independence.md,
  timing-interpretation.md).
- v0.7 (2026-07-06) — renamed role entry "Cockpit system" → "Technical Trader
  Solution"; updated anti-synonyms (added `cockpit system` retired, removed
  `solution`); updated prohibition note; updated tech-restricted preamble and
  Theme note. Client-project feedback: receiving agents confused by "cockpit".
  Historical changelog entries preserved unchanged.
- v0.6 (2026-07-06) — added Bond cohort (new standard entry): a transitively
  bonded set of tickers, purely structural, independent of detection timing
  or trader judgment — distinct from candidate net (a trader solution-level
  artifact) and theme (requires an accepted connection). Driven by MB-007
  authoring, where "group of tickers" was found to be under-specified for
  this specific structural-emergence concept.
- v0.5 (2026-07-06) — resolved CLARIF-001 (trader clarification): "group" in
  correlation-framework.md §2.1–2.2 confirmed as plain-English generic
  (two-or-more tickers), no domain-specific meaning. Added usage convention
  to the Group entry — write "group of tickers" in full, never bare "group",
  when this sense is meant.
- v0.4 (2026-07-06) — added Common-terms pointer rule: ambiguous common-status
  term usage (no domain term's anti-synonyms confirm safe substitution) routes
  to authoring-hygiene Rule 8 stop-and-report, not silent plain-English
  substitution. Driven by a test-run finding on correlation-framework.md §2.1.
- v0.3 (2026-07-06) — vocabulary gate pass on 2026-07-02 snapshot. Replaced
  "Domain terms — trader to define" placeholder section with "Domain terms —
  standard" section (22 new standard entries: theme, candidate net, sync, sync
  rank, bonding strength, pair bond, bond/bonding, bond network, connection,
  structural resemblance, curated theme, dynamic theme, emergent theme, market
  independence, Type 1, Type 2, Type 3, conviction, setup, confluence,
  performance breadth, intraday setup density, narrative formation, eligible
  universe). Added "Common terms" section (group, tag, scheme, category).
  Added ADR and wld to tech-restricted section. Updated growth rule with
  authoring-skill fallback behavior. Dynamic theme added as a new entry
  emergent from trader notes. All other entries derived from trader decisions
  in term-proposals-2026-07-02.md.
- v0.2 (2026-07-03) — removed Runtime agent entry (AI is implementation, not
  role); renamed System → Cockpit system; added tech-restricted category
  covering agent/LLM/AI/API/database/service/framework; added bare "cockpit"
  to Cockpit-system anti-synonyms and extended rule note.
- v0.1 (2026-07-02) — initial draft; seeded roles, banlist, and placeholders
  for parent-project domain terms.
