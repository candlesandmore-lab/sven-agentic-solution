# Term proposals — 2026-07-02
Status: PROCESSED
<!-- All 27 terms resolved by trader and written to glossary v0.3. -->

Computed thresholds: single nouns >= 5 | compound noun-phrases >= 3
Files scanned: 6

File abbreviations:
- BI  = docu/snapshot/2026-07-02/belief/BELIEF-INDEX.md
- CF  = docu/snapshot/2026-07-02/belief/correlation-framework.md
- FL  = docu/snapshot/2026-07-02/belief/filtering-logic.md
- TI  = docu/snapshot/2026-07-02/belief/timing-interpretation.md
- MI  = docu/snapshot/2026-07-02/belief/market-independence.md
- CUS = docu/snapshot/2026-07-02/cockpit-user-stories.md

---

## [group]
Glossary status: placeholder
Frequency: 80+ across 5 files

**SPLIT CANDIDATE — critical internal conflict**
FL:L13 states "The terms 'theme' and 'group' are used interchangeably." The glossary lists them as distinct placeholder terms. CUS P1 (L38–43) uses "group" in a different sense: the bond-network connected component before trader approval, whereas a "theme" is the trader-approved version. Two distinct meanings appear to coexist.

Sample usages (up to 5):
1. [FL:L13] — "The terms 'theme' and 'group' are used interchangeably."
2. [FL:L9] — "A theme is a group of tickers that move together in a synchronized way due to a shared connection..."
3. [CUS:L40] — "A theme is a trader-approved group with a confirmed meaningful connection. These are distinct first-class concepts."
4. [CF:L83] — "Sync rank measures ongoing group cohesion — how bonded tickers are to each other and to the theme over a sustained period."
5. [CF:L259] — "Group label and member count / Performance dispersion across members..."

Proposed definition:
Two senses are present. Sense A (FL usage): bare synonym for theme — "group" and "theme" mean the same thing and are used interchangeably. Sense B (CUS P1 usage): a connected component of tickers in the bond network that has not yet been trader-approved as a theme — the raw behavioral grouping before conviction. The glossary currently treats group and theme as distinct, which matches Sense B but conflicts with Sense A. Resolution from the trader is required before either sense can be used authoritatively in deliverables.

Proposed anti-synonyms: candidate net, cluster, basket (in either sense), theme

Confidence: low
- Usages are inconsistent across files. FL uses group and theme interchangeably; CUS P1 distinguishes them explicitly.

Open questions:
- Is "group" a genuine synonym for "theme" in the trader's vocabulary, or does FL:L13 represent informal usage that should be standardized away?
- If Sense B is the intended meaning (bond-network connected component before approval), what is the approved term for it? "Candidate net" covers a specific subset (new threshold-crossings); does a broader term for the pre-approval grouping exist?
- Can bare "group" ever be used safely, or does it always need qualification?

Trader decision: COMMON 
Trader notes: "The terms 'theme' and 'group' are not interchangeably in the context of this project. Any other statement is wrong. A group is just that - a group tickers WITHOUT any further bearing."

---

## [theme]
Glossary status: placeholder
Frequency: 100+ across 5 files

Sample usages (up to 5):
1. [FL:L9] — "A theme is a group of tickers that move together in a synchronized way due to a shared connection that causes institutional money to buy or sell them in proximity."
2. [FL:L25] — "A surfaced candidate net is never automatically a theme — regardless of how strong or how many signals produced it."
3. [FL:L29] — "Only trader confirmation of a meaningful connection converts a candidate net into a theme."
4. [CF:L163] — "Curated themes — manually maintained by the trader over time, anchored to a durable real-world connection..."
5. [CUS:L38] — "A theme is a trader-approved group with a confirmed meaningful connection."

Proposed definition:
A trader-approved collection of tickers sharing a confirmed connection — grounded in concrete company-level facts — that explains why institutional money buys or sells them together. Requires both observed behavioral sync and a confirmed connection; either alone is insufficient. A theme has a lifecycle (formation, strengthening, peak sync, breakout, dissolution) and its membership is defined by observed co-movement and trader judgment, not by classification systems. Two sub-types exist: curated themes (manually maintained, durable) and emergent themes (behaviorally surfaced, lifecycle-driven).

Proposed anti-synonyms: candidate net, group (if SPLIT decision applies), sector, topic, watchlist, group

Confidence: high
- Definition is stated explicitly and consistently across FL and CUS. The main ambiguity is the group/theme relationship, which is a separate entry.

Open questions:
- Resolve group/theme SPLIT decision first — the theme definition depends on whether "group" is a synonym or a distinct concept.
- Confirm whether "dynamic theme" (CUS usage, e.g. US-3.3) is synonymous with "emergent theme" (CF §2.8 usage) or a separate concept.

Trader decision: REDEFINE
Trader notes: "A trader-approved collection of tickers sharing a confirmed connection — grounded in concrete company-level facts — that may explain why institutional money buys or sells them together. Requires both observed behavioral sync and a confirmed connection; either alone is insufficient. A theme has a self-repeating lifecycle (formation, strengthening, peak sync, breakout, dissolution) and its membership is defined by observed co-movement and trader judgment, not by classification systems."

---

## [candidate net]
Glossary status: placeholder
Frequency: 25+ across 2 files

Sample usages (up to 5):
1. [FL:L25] — "A surfaced candidate net is never automatically a theme — regardless of how strong or how many signals produced it."
2. [CUS:L244] — "The system automatically finds the largest connected group among new threshold crossings (candidate net) rather than showing isolated pairs."
3. [CUS:L250] — "Each candidate net shown with: member tickers, similarity scores, wld(s) where threshold was crossed, thumbnail charts."
4. [CUS:L253] — "Candidate nets ordered by bond strength (trader-selectable sort)."
5. [FL:L28] — "Behavioral co-movement can arise from noise, coincidence, shared index/beta exposure, or sector-wide drift with no specific connection behind it. Surfacing is an invitation to investigate, not a claim of theme-hood."

Proposed definition:
The largest connected component of tickers whose pairwise similarity scores newly crossed the detection threshold in a given nightly batch run. A candidate net is the automated surface — an invitation to investigate — never a theme. Trader confirmation of a meaningful connection is required to convert it into a theme. Multiple candidate nets may be surfaced per batch run and may be ordered by aggregate bond strength.

Proposed anti-synonyms: theme, group, watchlist, universe, cluster, group

Confidence: high
- Usage is consistent across FL and CUS; definition is clearly implied by usage context.

Open questions:
- Does "candidate net" apply only to newly detected nets (new threshold crossings) or does it also refer to previously surfaced but unresolved candidate groupings?
- Is there a distinct term for the broader bond-network connected component that is not specific to a single batch run's new crossings?

Trader decision: REDEFINE
Trader notes: "The largest connected component of tickers whose pairwise similarity scores newly crossed the detection threshold in a given nightly batch run. A candidate net is the automated surface — an invitation to investigate — never a theme. Trader confirmation of a meaningful connection is required to convert it into a theme. Multiple candidate nets may be surfaced per batch run and may be ordered by aggregate bond strength."

---

## [tag]
Glossary status: placeholder
Frequency: 2 across 1 file

**Note: this term appears to be retired.** CUS P3 explicitly marks it as historical usage.

Sample usages (up to 5):
1. [CUS:L56] — "Trader-created themes (previously called 'tags' in SARMOCONIA) and cockpit-detected emergent themes are the same object living in the same collections managed by ThemeTagsHub."

Proposed definition:
Historical label for trader-created themes in the SARMOCONIA system prior to the single-theme-concept decision (P3). As of CUS v0.3 (Session 41), "tag" was retired in favour of the unified "theme" concept. The term does not appear to carry active meaning in the current corpus.

Proposed anti-synonyms: scheme, category, label (all potentially retired alongside it)

Confidence: medium
- Only one explicit snapshot usage; that usage explicitly frames it as legacy terminology.

Open questions:
- Is "tag" fully retired as an active term, or does it still appear in any live SARMOCONIA code, collections, or UI labels that deliverables must reference?
- If fully retired, should the glossary entry be changed to status `retired` rather than `placeholder`?

Trader decision: CONFIRM
Trader notes: <!-- edits, corrections, or redefinition here -->

---

## [scheme]
Glossary status: placeholder
Frequency: 0 across 0 files

**Note: not found in any snapshot file.** The glossary lists it as a placeholder but no usage was detected in the 2026-07-02 snapshot.

Sample usages: none found.

Proposed definition: unable to infer — no snapshot usages.

Proposed anti-synonyms: tag, category, taxonomy (from glossary pre-population)

Confidence: low
- No evidence in snapshot. Cannot propose a definition.

Open questions:
- Does "scheme" appear in undocumented source material (e.g. system-design docs outside the snapshot), or can this entry be retired from the glossary?
- If it refers to a tagging or categorization scheme within SARMOCONIA, is that distinct from what "tag" or "category" describes?

Trader decision: COMMON
Trader notes: "does not bear any meaning in the corpus"

---

## [category]
Glossary status: placeholder
Frequency: 3 across 2 files

Sample usages (up to 5):
1. [FL:L39] — "The bar for a valid connection is not about how broad or narrow the category is — it is about directionality."
2. [FL:L42] — "Membership in a narrow industry classification is not, by itself, a connection. Tickers sharing only an industry tag — for example, all classified under 'Uranium' — are not automatically a theme; the tag must not become a substitute for an actual explanation..."
3. [FL:L48] — "A connection is supported when these concrete facts...tell a coherent story explaining possibly shared institutional buying or selling interest — not when tickers merely resemble each other by classification or surface description."

Proposed definition:
Used in FL exclusively in its ordinary English sense — broad grouping by shared attribute. No domain-specific meaning is attached; it appears only as a counterexample to what a valid theme connection is not. May qualify as COMMON rather than requiring a domain definition.

Proposed anti-synonyms: (none domain-specific found)

Confidence: medium
- Usages are consistent but generic. The glossary flags it as load-bearing alongside tag and scheme, but snapshot evidence does not support a domain-specific definition.

Open questions:
- Is "category" used with a distinct domain meaning elsewhere (e.g. in system-design docs or UI) that would require a definition here?
- Can this entry be marked COMMON (not specialized in this corpus)?

Trader decision: COMMON
Trader notes: <!-- edits, corrections, or redefinition here -->

---

## [sync]
Glossary status: absent
Frequency: 60+ across 4 files

Sample usages (up to 5):
1. [CF:L11] — "All detectable sync signals are manifestations of the same underlying phenomenon: two or more tickers moving similarly during the same period for a non-random reason."
2. [FL:L17] — "Observed behavioral sync — price/volume co-activation, synchronized range behavior, structural resemblance across members."
3. [CF:L14] — "The three signal types are not lifecycle stages. They are independent expressions of group bonding that can occur at any point..."
4. [FL:L91] — "Co-activations become more frequent and more consistent in direction. Range behavior begins to synchronize..."
5. [CF:L83] — "Sync rank measures ongoing group cohesion — how bonded tickers are to each other and to the theme over a sustained period."

Proposed definition:
Observable behavioral co-movement between two or more tickers during the same period, arising from a non-random shared cause. Sync manifests in three types (Type 1: spike co-activation; Type 2: momentum density with resemblance; Type 3: structural resemblance). Sync is a necessary but not sufficient condition for theme conviction — a confirmed connection is also required.

Proposed anti-synonyms: correlation (strict statistical sense), co-movement (weaker — does not imply a non-random cause), resemblance (partial — structural resemblance is one type of sync, not the whole)

Confidence: high
- Used consistently throughout CF and FL with clear domain meaning. Distinct from statistical correlation (banlisted).

Open questions:
- Is "sync" always shorthand for "behavioral sync," or are there usages where it refers to a narrower or different concept?
- Should "sync" appear as a standalone glossary entry, or only in qualified forms (behavioral sync, sync rank, sync signal)?

Trader decision: REDEFINE
Trader notes: "Observable behavioral co-movement between two or more tickers during the same period, regardless of the existence of a shared cause. Sync manifests in three types (Type 1: spike co-activation; Type 2: momentum density with resemblance; Type 3: structural resemblance). Sync is a necessary but not sufficient condition for theme conviction — a confirmed connection is also required."

---

## [sync rank]
Glossary status: absent
Frequency: 20+ across 3 files

Sample usages (up to 5):
1. [CF:L83] — "Sync rank measures ongoing group cohesion — how bonded tickers are to each other and to the theme over a sustained period."
2. [CF:L92] — "A tight flag/base period with high visual resemblance across members but no spikes ranks higher than a group with strong spikes but no sustained resemblance between them."
3. [CF:L98] — "Sync rank is a condition that makes the group worth watching — it is not a signal to act on by itself."
4. [CF:L372] — "Sync rank modulates trade selectivity. It does not replace setup quality as the trigger."
5. [CUS:L103] — "Y-axis: bonding strength (aggregate resemblance score across approved members)" [cf. sync rank — see open questions]

Proposed definition:
A measure of ongoing group cohesion: how tightly bonded theme members are to each other over a sustained period. Driven primarily by Type 2 and Type 3 sync signals; Type 1 (spikes) contributes but cannot drive the ranking alone. Not a price-move predictor — high sync rank means the group is currently moving together; it says nothing about timing or direction of any subsequent move.

Proposed anti-synonyms: score (generic), rating, price-move signal, momentum indicator

Confidence: high
- CF §2.3 defines it explicitly and consistently. Distinct from bonding strength (see open question).

Open questions:
- CUS US-1.1 uses "bonding strength" as the Y-axis label where sync rank might be expected. Are "sync rank" and "bonding strength" synonymous, two different measurements, or one aggregated from the other?
- Is sync rank a per-pair measure, a per-theme measure, or both?

Trader decision: REDEFINE
Trader notes: ""sync rank" and "bonding strength" are synonymous. A measure of ongoing group cohesion strength: how tightly bonded a group of tickers (>= 2 members) are to each other over a sustained period. Driven by all 3 sync types. Not a price-move predictor — high sync rank means the group is currently rather closely moving together; it says nothing about timing or direction of any subsequent move.
Is applied to a single ticker pair (answering the question how strong the pair bond is) and in aggregated form for candidate nets and themes."

---

## [pair bond]
Glossary status: absent
Frequency: 30+ across 3 files

Sample usages (up to 5):
1. [FL:L58] — "Theme formation typically begins with a single pair bond — two tickers showing behavioral similarity during the same period."
2. [CF:L118] — "The pair is the natural unit of bonding. Two tickers either show evidence of moving together for a non-random reason or they don't."
3. [CUS:L40] — "Themes grow incrementally from pair bonds; the bond network is the source material from which themes emerge through trader judgment."
4. [FL:L60] — "This is not a group appearing at once; it is the first observable connection between two tickers."
5. [CF:L122] — "When pair A–B is bonded, pair B–C is bonded, and pair A–C is bonded, the trader sees a group {A, B, C}."

Proposed definition:
An observed pairwise sync signal between two specific tickers that is strong enough and sustained enough to constitute evidence of a non-random connection between them. The pair bond is the atomic unit from which themes emerge — a theme requires at minimum one confirmed pair bond plus a confirmed connection. Bond evidence accumulates per pair across signal types and across time.

Proposed anti-synonyms: theme (a theme requires trader approval and a connection; a pair bond is evidence, not a conclusion), group, connection (a connection is the explanatory link; a pair bond is the behavioral evidence)

Confidence: high
- Used consistently as the foundational detection unit throughout FL and CF.

Open questions:
- Is there a threshold that distinguishes "a pair bond exists" from "the pair shows some sync"? The snapshot describes threshold-crossing (CUS US-3.1) — is that threshold the definition of a pair bond existing?
- Is "bond" alone (without "pair") used interchangeably with "pair bond," or does bare "bond" refer to something broader?

Trader decision: REDEFINE
Trader notes: "An observed sync rank between two specific tickers that is above a threshold and sustained enough to indicate evidence of a non-random connection between them. Theoretically there is a pair bond between every 2 tickers and the sync rank is the measure of their relative strength vs other pair bonds."

---

## [bond / bonding]
Glossary status: absent
Frequency: 60+ across 4 files

Sample usages (up to 5):
1. [CF:L118] — "The pair is the natural unit of bonding. Two tickers either show evidence of moving together for a non-random reason or they don't."
2. [CF:L125] — "Evidence of bonding is accumulated per pair across signal types and across time — a Type 1 spike co-activation in one window and Type 3 structural resemblance in another window are stronger combined evidence than either alone."
3. [CUS:L103] — "Y-axis: bonding strength (aggregate resemblance score across approved members)"
4. [CUS:L165] — "per-ticker bonding contribution to the group"
5. [FL:L63] — "Additional members accumulate over subsequent sessions as further pair bonds form with existing members or as AI reasoning suggests plausible tickers based on the confirmed connection."

Proposed definition:
The state of accumulated pairwise sync evidence between two tickers across signal types and time. "Bonding" is the process; "bond" is the resulting state. Bonding is the verb/noun form of pair bond and is used at two levels: (a) pairwise — does a bond exist between ticker A and ticker B? and (b) theme-level — how strongly do theme members bond with each other in aggregate (bonding strength)?

Proposed anti-synonyms: correlation (strict), pairing, linking

Confidence: high
- Consistent usage. Treat as the base form from which "pair bond" and "bonding strength" derive.

Open questions:
- Should "bond" / "bonding" have its own glossary entry, or should it be a cross-reference under the "pair bond" and "bonding strength" entries?

Trader decision: REDEFINE
Trader notes: "The state of accumulated pairwise sync evidence between two tickers across signal types and time. "Bonding" is the process usually indicating an increasing sync rank; there is always a "bond" between tickers or groups of tickers, what differs is the sync rank or aggregated sync rank for groups. Bonding is the verb/noun form of bond and is used at two levels: (a) pairwise — does a bond exist between ticker A and ticker B? and (b) theme-level — how strongly do theme members bond with each other in aggregate (bonding strength)?"

---

## [bond network]
Glossary status: absent
Frequency: 20+ across 3 files

Sample usages (up to 5):
1. [CUS:L40] — "The bond network is the living state of observed pairwise similarities across all eligible tickers — a computational artifact that changes nightly. A theme is a trader-approved group with a confirmed meaningful connection. These are distinct first-class concepts."
2. [CUS:L291] — "US-3.4 — Bond Network Graph View"
3. [CUS:L307] — "Right-click on any node opens the assignment dialog: add to existing theme, create new theme, discard for specific theme(s)"
4. [CF:L122] — "When pair A–B is bonded, pair B–C is bonded, and pair A–C is bonded, the trader sees a group {A, B, C}." [bond network implied]
5. [CUS:L318] — "General-purpose exploration mode, not tied to the morning workflow — available anytime"

Proposed definition:
The complete living state of all observed above-threshold pairwise similarities across eligible tickers at a given point in time. A computational artifact that is recalculated nightly. Explicitly distinct from any theme — the bond network is the raw material from which themes emerge through trader judgment and confirmed connections. Not a static structure; bonds appear and dissolve as tickers' behaviors change.

Proposed anti-synonyms: theme, group, graph (a graph visualization can represent the bond network but is not the bond network itself), watchlist

Confidence: high
- CUS P1 defines it explicitly. The distinction from theme is a hard constraint (CUS P1, first principle).

Open questions:
- None material. Definition is explicit in the source.

Trader decision: REDEFINE
Trader notes: "The complete living state of all pairwise synk ranks across eligible tickers at a given point in time. A computational artifact that is recalculated nightly. Explicitly distinct from any theme — the bond network is the raw material from which candidate nets will emerge and based on which any pair or group of tickers' (aggregated) sync rank can be computed. It the source of truth and is maintaining historical values."

---

## [bonding strength]
Glossary status: absent
Frequency: 15+ across 2 files

Sample usages (up to 5):
1. [CUS:L103] — "Y-axis: bonding strength (aggregate resemblance score across approved members)"
2. [CUS:L107] — "Bubble size encodes member count"
3. [CF:L72] — "whether bonding strength is predictive of future group price moves or only descriptive of current state"
4. [CUS:L165] — "per-ticker bonding contribution informs maintenance decisions (weakest ticker = drop candidate) and setup assessment (strongest tickers = likely leaders)"
5. [CUS:L399] — "per-ticker bonding contribution declining (weakest member)" [maintenance trigger]

Proposed definition:
An aggregate measure of how tightly a theme's members are currently moving together, computed from pairwise sync scores across approved members. Represents the theme-level cohesion. Used on the daily scatter (Y-axis) and in theme maintenance to identify weakening members. As of the snapshot, treated as descriptive only — whether it predicts future group moves is an open empirical question.

Proposed anti-synonyms: performance, momentum

Confidence: medium
- Used consistently but the relationship to "sync rank" is not resolved in the source material. CF uses "sync rank" where CUS uses "bonding strength" for what may be the same concept.

Open questions:
- Are "bonding strength" and "sync rank" synonymous? CUS US-1.1 uses "bonding strength" as the scatter Y-axis; CF §2.3 describes "sync rank" as the cohesion measure. If they differ, what is the distinction?
- Is bonding strength theme-level only, or is there also a pairwise bonding strength?

Trader decision: REDEFINE
Trader notes: ""sync rank" and "bonding strength" are the same concept!"

---

## [connection]
Glossary status: absent
Frequency: 35+ across 4 files

Sample usages (up to 5):
1. [FL:L17] — "A discovered connection that makes sense — something that explains why these tickers would be bought together by the same institutions at the same time."
2. [FL:L31] — "Only trader confirmation of a meaningful connection converts a candidate net into a theme."
3. [FL:L33] — "The bar for a valid connection is not about how broad or narrow the category is — it is about directionality. A specific, narrow shared activity within a broader sector is frequently a valid theme..."
4. [FL:L43] — "The connection's evidentiary basis is concrete company-level fact, not category inference: what each company makes or does, who it serves, and what is currently happening to it."
5. [CUS:L273] — "Trader selects a proposed connection (or writes custom), selects which tickers belong to the new theme..."

Proposed definition:
The explanatory link — grounded in concrete company-level facts — that justifies why institutional money would buy or sell a set of tickers together. A connection is required alongside observed behavioral sync to convert a candidate net into a theme. It does not need to be known before detection; it is confirmed or hypothesized after the behavioral signal is observed. Valid connections are directional (explain specific shared institutional interest) rather than categorical (mere industry-tag membership).

Proposed anti-synonyms: narrative (narrative is one input to finding a connection, not the connection itself), hypothesis (a hypothesis is a candidate connection before confirmation), category, sector, label

Confidence: high
- Used consistently with clear domain meaning throughout FL and CUS. The domain sense is specific enough to distinguish from common English "connection."

Open questions:
- Is "confirmed connection" the formal state, and "hypothesized connection" the unconfirmed state? The snapshot uses both framings — confirm whether these are the intended qualified forms.

Trader decision: "REDEFINE"
Trader notes: "The explanatory link — grounded in concrete company-level facts — that could justify why institutional money would buy or sell a set of tickers together. A connection is required alongside observed behavioral sync to convert a candidate net into a theme. It does not need to be known before detection; it is confirmed or hypothesized after the behavioral signal is observed. Connections establish an additional dimension to the static GCIS sectors and industries."

---

## [structural resemblance]
Glossary status: absent
Frequency: 15+ across 3 files

Sample usages (up to 5):
1. [CF:L54] — "Two tickers show visually similar chart structure during the same or adjacent periods — similar shape, rhythm, timing of pauses and pushes — regardless of absolute price magnitude."
2. [CF:L59] — "Sync is temporary and pairwise, may shift between which pair within a group is active."
3. [CF:L60] — "Market-condition agnostic — resemblance during selling periods is as informative as during buying periods."
4. [FL:L17] — "Observed behavioral sync — price/volume co-activation, synchronized range behavior, structural resemblance across members."
5. [BI:L29] — "correlation-framework.md: ... two kinds of themes (curated and emergent), §2.9 multi-perspective convergence/confluence belief" [structural resemblance central to Type 3]

Proposed definition:
The Type 3 sync signal — visual similarity between two tickers' chart shapes during the same or adjacent periods: similar shape, rhythm, and timing of pauses and pushes, regardless of absolute price magnitude. Resemblance is assessed pairwise. Market-condition agnostic — resemblance during selling periods carries the same informational weight as during buying periods.

Proposed anti-synonyms: correlation (strict statistical sense), similarity score (a computed score may measure structural resemblance but is not the same concept), co-movement (weaker — implies directionality; structural resemblance does not require same direction)

Confidence: high
- CF §2.2 Type 3 defines it explicitly. Consistent with usage in FL and BI.

Open questions:
- Is "structural resemblance" always pairwise (two tickers), or does it also apply at the group level?
- Does "resemblance" alone (without "structural") carry the same meaning in this corpus, or is the qualifier always required?

Trader decision: REDEFINE
Trader notes: "The Type 3 sync signal — visual similarity between two tickers' chart shapes during the same or adjacent periods: similar shape, rhythm, and timing of pauses and pushes, regardless of absolute price magnitude. Resemblance is assessed pairwise. Market-condition agnostic — resemblance during selling periods carries the same informational weight as during buying periods. "resemblance" alone (without "structural") carry the same meaning in this corpus but the latter should be used."

---

## [curated theme]
Glossary status: absent
Frequency: 8+ across 3 files

Sample usages (up to 5):
1. [CF:L163] — "Curated themes — manually maintained by the trader over time, anchored to a durable real-world connection (for example: stocks related to nuclear energy, or established sub-groupings within the biotech industry). These are stable, change slowly, and reflect the trader's accumulated knowledge of the market structure."
2. [CF:L172] — "Both are valid and both are worth watching."
3. [CUS:L98] — "Scatter displays all themes (single concept — no curated/dynamic distinction)" [note: UI hides the distinction, but the distinction exists in trader belief]
4. [CUS:L225] — "For curated themes: shows the existing description from the themes collection."
5. [BI:L29] — "correlation-framework.md: ... two kinds of themes (curated and emergent)"

Proposed definition:
A theme manually maintained by the trader over time, anchored to a durable real-world connection reflecting accumulated knowledge of market structure (e.g. nuclear energy stocks, established biotech sub-groupings). Curated themes are stable and change slowly. Contrasted with emergent themes, which are behaviorally surfaced and have a lifecycle. Both types share the same object definition and infrastructure (ThemeTagsHub).

Proposed anti-synonyms: emergent theme, dynamic theme, auto-detected theme

Confidence: high
- CF §2.8 defines it explicitly. Consistent with CUS usage.

Open questions:
- CUS uses "dynamic theme" where CF uses "emergent theme." Are these synonymous? If so, which term should be canonical in deliverables?
- Does the curated/emergent distinction need to surface in deliverable docs, or is the single-theme-concept decision (CUS P3) intended to suppress the distinction from the cockpit view while preserving it in belief documents?

Trader decision: REDEFINE
Trader notes: "A theme manually maintained by the trader over time, anchored to a durable connection reflecting accumulated knowledge of market structure (e.g. nuclear energy stocks, established biotech sub-groupings). Curated themes are existing themes in the existing database and maintained manually. Contrasted with dynamic themes, which are behaviorally surfaced and have a sync-rank driven lifecycle. Both types share the same object definition and infrastructure (ThemeTagsHub).
Conceptually, in the future curated themes may be fully replaced by dynamic themes."
---

## [emergent theme]
Glossary status: absent
Frequency: 6+ across 3 files

Sample usages (up to 5):
1. [CF:L167] — "Emergent themes — surfaced from currently observed behavioral bonding among tickers that may not share an obvious or pre-existing label. These have a lifecycle (Section 1.2): they form, strengthen, peak, dissolve. They are alive in a way that curated themes are not."
2. [BI:L29] — "correlation-framework.md: ... two kinds of themes (curated and emergent)"
3. [CUS:L55] — "cockpit-detected emergent themes are the same object living in the same collections managed by ThemeTagsHub"
4. [CF:L172] — "Emergent themes give the trader the early-stage edge described in Section 1.4 — visibility into bonding that hasn't yet shown up in standard screeners."
5. [CUS:L54] — "Trader-created themes (previously called 'tags' in SARMOCONIA) and cockpit-detected emergent themes are the same object..."

Proposed definition:
A theme surfaced from currently observed behavioral bonding among tickers that may not share an obvious or pre-existing label. Emergent themes have a lifecycle (formation, strengthening, peak sync, breakout, dissolution). They are "alive" — dynamic — in a way that curated themes are not. Emergent themes provide the early-stage detection edge that morning screeners structurally miss (FL §1.4). Also referred to as "dynamic theme" in CUS — see open question.

Proposed anti-synonyms: curated theme, sector group, screener result, dynamic theme (they are dynamic themes that are observed for the first time (= emerging))

Confidence: high
- CF §2.8 defines it explicitly.

Open questions:
- Is "emergent theme" (CF §2.8 belief term) synonymous with "dynamic theme" (CUS implementation term)? If so, which should be the canonical term in deliverables?
- CUS P3 states that "cockpit-detected emergent themes" and "trader-created themes" are the same object. Does "emergent theme" in deliverables always mean cockpit-surfaced, or can a trader manually create an emergent theme?

Trader decision: REDEFINE
Trader notes: "A theme surfaced from currently observed, increasing behavioral bonding among tickers that may not share an obvious or pre-existing label. They are dynamic themes that are observed for the first time (= emerging). Emergent themes provide the early-stage detection edge that morning screeners structurally miss (FL §1.4)."

---

## [market independence]
Glossary status: absent
Frequency: 8+ across 3 files

Sample usages (up to 5):
1. [MI:L11] — "The baseline for any sync signal is the indexes — SPY, QQQ, IWM. If two tickers resemble each other but both also resemble the index during the same window, the signal is market-driven, not group-specific."
2. [CF:L137] — "The genuinely informative signal: tickers resembling each other while diverging from the indexes."
3. [CF:L143] — "A pair only counts as a group signal if it stands apart from the relevant index in the same window."
4. [MI:L26] — "Pair resembles each other AND resembles SPY/QQQ/IWM → beta signal, low value"
5. [MI:L28] — "Pair resembles each other AND diverges from SPY/QQQ/IWM → group signal, high value"

Proposed definition:
The property of a pair sync signal that holds when two tickers show mutual resemblance while simultaneously diverging from the relevant broad-market index (SPY/QQQ/IWM) in the same window. A market-independent sync signal is high-value because it indicates group-specific institutional activity rather than index beta. A pair that resembles both each other and the index produces a low-value, index-explained signal. Market independence is not a separate analytical step — it is assessed as part of the same observation as the sync signal itself.

Proposed anti-synonyms: beta signal (the index-driven counterpart), index co-movement, sector-wide drift

Confidence: high
- MI and CF §2.6 are consistent and explicit.

Open questions:
- What index is the appropriate baseline per market cap tier? MI flags this as open: IWM for small caps, QQQ for NASDAQ names, SPY as broad baseline. => practical approximation: QQQ for NASDAQ exchange traded names, SPY for rest 
- Is there a threshold for how much divergence from the index is required to qualify as group-specific, or is it a qualitative judgment? => there is no generic level; question to be answered by user stories

Trader decision: CONFIRM
Trader notes: <!-- edits, corrections, or redefinition here -->

---

## [Type 1 / Type 2 / Type 3]
Glossary status: absent
Frequency: 40+ across 3 files (all three types combined)

Sample usages (up to 5):
1. [CF:L27] — "Type 1 — Spike Co-activation: Two or more tickers show sharp price/volume spikes within ±2-3 days of each other, in the same direction."
2. [CF:L38] — "Type 2 — Momentum Density with Resemblance: Sustained directional momentum with elevated volume over multiple weeks — 'volume density.'"
3. [CF:L54] — "Type 3 — Structural Resemblance: Two tickers show visually similar chart structure during the same or adjacent periods..."
4. [CF:L14] — "The three signal types are not lifecycle stages. They are independent expressions of group bonding that can occur at any point..."
5. [CUS:L15] — "C1 — MVP: Type 3 resemblance only, graph model, basic visualization, backfill, AI-agent connection determination"

Proposed definition (three linked entries):
- **Type 1 (spike co-activation):** Two or more tickers show sharp price/volume spikes within ±2–3 days of each other in the same direction. Primary for pair activation and event-based confirmation. Contributes to sync ranking but cannot drive it alone.
- **Type 2 (momentum density with resemblance):** Sustained directional momentum with elevated volume over multiple weeks ("volume density"), manifesting as pairwise structural resemblance within a larger group. The higher-energy, directional version of Type 3; inherently includes the resemblance component.
- **Type 3 (structural resemblance):** Visually similar chart structure between two tickers during the same or adjacent periods — similar shape, rhythm, timing of pauses and pushes — regardless of price magnitude or direction. Market-condition agnostic; temporary and pairwise.

The three types are independent expressions of group bonding, not lifecycle stages. Multiple types can co-occur and confirm each other (§2.4 multi-signal confirmation).

Proposed anti-synonyms: phases, stages, levels (they are types, not a sequence)

Confidence: high
- Explicitly defined in CF §2.2. Consistent usage throughout.

Open questions:
- Should Type 1, Type 2, Type 3 be three separate glossary entries cross-linking each other, or one combined entry?
- C1 MVP implements Type 3 only. Should the other types be marked as out-of-scope for the C1 deliverable context?

Trader decision: REDEFINE
Trader notes: 
"- **Type 1 (spike co-activation):** Two or more tickers show sharp price/volume spikes within ±2–3 days of each other in the same direction. Primary for pair activation and event-based confirmation. 
- **Type 2 (momentum density with resemblance):** Sustained directional momentum with elevated volume over multiple weeks ("volume density"), manifesting as pairwise structural resemblance within a larger group. The higher-energy, directional version of Type 3; inherently includes the resemblance component.
- **Type 3 (structural resemblance):** Visually similar chart structure between two tickers during the same or adjacent periods — similar shape, rhythm, timing of pauses and pushes — regardless of price magnitude or direction. Market-condition agnostic; temporary and pairwise.
3 separate glossary entries suggested.
"

---

## [conviction]
Glossary status: absent
Frequency: 10+ across 3 files

Sample usages (up to 5):
1. [FL:L16] — "Conviction to trade a theme requires two things in combination: 1. Observed behavioral sync... 2. A discovered connection that makes sense..."
2. [FL:L18] — "Neither alone is sufficient. Sync without a connection is noise...A connection without sync is just a list — interesting but not actionable."
3. [CF:L372] — "Sync Level as Conviction Modifier: Sync rank modulates trade selectivity. It does not replace setup quality as the trigger."
4. [CF:L375] — "High sync rank + confirmed connection → accept 3-star setups that would otherwise be skipped."
5. [CF:L179] — "multiple, genuinely independent observations of the same theme, each derived from a structurally different dimension of ticker-associated data — increases conviction that the theme is entering or approaching an active move"

Proposed definition:
The trader's basis for acting on a theme — for committing attention, watchlist placement, and ultimately trade consideration. Conviction requires both observed behavioral sync and a confirmed connection; neither alone is sufficient. Conviction is modulated by sync rank (a higher sync rank lowers the setup quality bar required to enter) and increased by confluence of multiple independent observation dimensions (§2.9). Conviction is never a computed score — it is a trader judgment.

Proposed anti-synonyms: confidence score, probability, rank, rating (conviction is a judgment, not a metric)

Confidence: high
- Used consistently with clear domain meaning. The dual-requirement structure is explicit.

Open questions:
- Does "conviction" in deliverables always refer to the trader's readiness to act, or does it also describe the strength of belief that a theme exists (pre-trading decision)?

Trader decision: REDEFINE
Trader notes: "The trader's basis for acting on a theme — for committing attention, watchlist placement, and ultimately trade consideration. Conviction requires both observed behavioral sync and a confirmed connection; neither alone is sufficient. Conviction is modulated by sync rank (a higher sync rank lowers the setup quality bar required to enter) and increased by confluence of multiple independent observation dimensions (§2.9). Conviction is never a computed score — it is a trader judgment.
"conviction" in deliverables refer to the trader's mental readiness to act and also describe the strength of belief that a theme exists (pre-trading decision)".
---

## [ADR]
Glossary status: absent
Frequency: 6+ across 3 files

Sample usages (up to 5):
1. [FL:L143] — "ADR > 3.5%" [as screening filter]
2. [CF:L256] — "ADR-normalized group averages are the natural performance measure (already produced by the trader's existing baseline pipeline)."
3. [CUS:L103] — "X-axis: group performance (ADR-normalized average across members)"
4. [CUS:L399] — "count and list of members currently below universe filters (ADR, price, sector)"
5. [FL:L141] — "Price > MA50 (always) / ADR > 3.5%" [in screening criteria list]

Proposed definition:
Average Daily Range — a measure of a ticker's typical intraday price movement expressed as a percentage of price. Used as: (a) a universe screening filter (minimum ADR > 3.5% to ensure sufficient daily movement for pattern detection), and (b) a normalization factor for group performance comparisons across tickers with different price levels and volatility profiles.

Proposed anti-synonyms: ATR (Average True Range — a related but distinct measure), volatility (generic — ADR is a specific calculation)

Confidence: high
- Usage is consistent and the meaning is unambiguous in trading context.

Open questions:
- Is ADR tech-restricted (implementation-side calculation) or a belief-level concept the trader reasons about directly? The screening criteria in FL §1.4 suggest the trader uses it as a primary filter criterion, which argues for belief-level status.

Trader decision: CONFIRM
Trader notes: ADR is tech-restricted. A comparable wording in MB and strategy docs should use "volatility" instead.

---

## [wld]
Glossary status: absent
Frequency: 20+ across 2 files

Sample usages (up to 5):
1. [CUS:L151] — "Changeable period length across all charts simultaneously: fixed toggles (14D / 21D / 35D)"
2. [CUS:L658] — "encode today's charts for all eligible tickers + all theme members regardless of filter status, at all wld"
3. [CUS:AF-2] — "per-pair per-wld per-day raw cosine scores + composite bond strength. EWMA spans wld×1.5"
4. [CUS:AF-8] — "bar_timeframe as first-class template field — determines embedding class, retention scope (126 days for D, 18 days for 1H)"
5. [CUS:L376] — [pairwise sync rank store context using wld as index dimension]

Proposed definition:
Window length in days — the lookback period parameter for chart encoding and pairwise similarity computation. Three values are used: 14D, 21D, 35D. Each wld produces a separate similarity score per ticker pair. The wld is a first-class dimension of the pairwise sync rank store (per-pair × per-wld × per-day). Primarily an implementation-level concept but the trader selects wld interactively in the pattern hunt and drill-down surfaces.

Proposed anti-synonyms: timeframe (broader — timeframe also includes bar type D/1H; wld is the bar count only), period (ambiguous — wld is specifically the window length used for encoding)

Confidence: medium
- Term is consistent but usage is mixed between implementation context (CUS architecture flags) and trader-facing selection (chart view toggles). Whether it belongs in belief-level or tech-restricted status is unclear.

Open questions:
- Is "wld" tech-restricted (implementation abbreviation that should not appear in market-behavior or trading-strategy deliverables) or a trader-facing concept that appears in user-story functional content?
- Is the full form "window length in days" the canonical expansion, or does the trader use a different phrase?

Trader decision: CONFIRM
Trader notes: term is technically restricted. strategies and user stories my use rolling window length instead. 

---

## [eligible universe]
Glossary status: absent
Frequency: 8+ across 2 files

Sample usages (up to 5):
1. [FL:L141] — "Price > MA50 (always) / ADR > 3.5% / Rank > 95th or 97th percentile / Group in top 30-40% across 5-62D timeframes / At least one major volume spike within last ~60 days"
2. [CUS:L333] — "Multi-select ticker dropdown populated from the eligible universe"
3. [CUS:L658] — "encode today's charts for all eligible tickers + all theme members regardless of filter status"
4. [CUS:L507] — "Handles new tickers entering and existing tickers leaving the eligible universe"
5. [CUS:L399] — "count and list of members currently below universe filters (ADR, price, sector) — visible at a glance as a theme health indicator"

Proposed definition:
The set of tickers that currently meet the trader's screening filters (ADR, price relative to MA, rank percentile, volume history) and are included in nightly batch encoding and pairwise computation. Theme members that fall below universe filters are tracked but not removed automatically — they remain in encoding and pairwise computation. "Universe" alone is also used interchangeably.

Proposed anti-synonyms: watchlist (the watchlist is a subset or output; the universe is the full eligible set), theme (a theme is a trader-approved subset of the universe)

Confidence: high
- Usage is consistent. The filters defining it are spelled out explicitly in FL §1.4.

Open questions:
- Are "eligible universe" and "universe" used interchangeably, or does "universe" alone sometimes mean something narrower (e.g. the tickers visible in a specific surface)?

Trader decision: CONFIRM
Trader notes: "eligible universe" and "universe" are synonymous relating to the group of tickers that are eligible for analysis.

---

## [setup]
Glossary status: absent
Frequency: 8+ across 3 files

Sample usages (up to 5):
1. [CF:L301] — "Assess whether sync is accompanied by an actionable setup — tightening range, flag, base forming. Always the trader's eyes, never automated."
2. [CF:L375] — "High sync rank + confirmed connection → accept 3-star setups that would otherwise be skipped."
3. [FL:L117] — "Chart structure and trader judgment determine whether there is a trade." [setup implied]
4. [CUS:L145] — "assess setup quality" [in US-2.1 thumbnail view context]
5. [CUS:L404] — "strongest tickers = likely leaders" [in context of setup assessment within a theme]

Proposed definition:
A chart configuration that, in the trader's judgment, offers a defined trade entry opportunity — characterized by specific structural conditions such as a tightening range, flag formation, base, or ledge. A setup is always assessed by trader eyes and never automated. Setup quality is a prerequisite for entry; sync rank modulates how high the setup quality bar must be (§3.6), but does not replace it.

Proposed anti-synonyms: signal (a signal may indicate that a setup might be forming; a setup is the confirmed chart configuration), trigger (the trigger is the break, not the setup itself), pattern (strict statistical sense — banlisted; use "setup" or "chart configuration" instead)

Confidence: high
- Consistent usage with clear trading-specific meaning distinct from common English "setup" (which implies configuration or preparation).

Open questions:
- Is "setup" tech-restricted from market-behavior or trading-strategy deliverables, or is it a trader belief concept that belongs in those docs? Given that it appears in CF §3 (trader-intent section), it appears to be belief-level.

Trader decision: CONFIRM
Trader notes: usable at belief level

---

## [confluence]
Glossary status: absent
Frequency: 3 across 1 file

Sample usages (up to 5):
1. [CF:L183] — "confluence — multiple, genuinely independent observations of the same theme, each derived from a structurally different dimension of ticker-associated data — increases conviction that the theme is entering or approaching an active move when several activate together."
2. [CF:L187] — "No single observation, including bond strength itself, is ever sufficient alone. The dimensions are orthogonal by construction: each must be derivable from a domain or lens that the others cannot explain away."
3. [BI:L29] — "§2.9 multi-perspective convergence/confluence belief"

Proposed definition:
The state in which multiple genuinely independent observation dimensions — bond cohesion, intraday setup density, performance breadth, narrative formation — activate together for the same theme. Confluence increases the trader's conviction that the theme may be approaching an active move, beyond what any single dimension signals. The dimensions are never combined into a single score or weighted composite; the trader reads the combination and decides. As of the snapshot, confluence is a working hypothesis not yet empirically validated.

Proposed anti-synonyms: convergence (tactical sense), composite score, weighted average, combined signal, aggregate metric (confluence is explicitly not a computed combination)

Confidence: medium
- CF §2.9 introduces it explicitly but flags it as a working hypothesis. Usage is limited to one file; the concept may not yet appear in other source material.

Open questions:
- Is "confluence" the canonical term for this concept, or does the trader also use "convergence" (BI:L29 uses "convergence/confluence")? If both are used, which is preferred for deliverables?
- Given that this is flagged as a working hypothesis, should deliverable docs present it with a hedge, or treat it as confirmed belief?

Trader decision: REDEFINE
Trader notes: "The state in which multiple genuinely independent observation dimensions — bond cohesion, intraday setup density, performance breadth, narrative formation — activate together for the same group of tickers like candidate nets or theme. Confluence increases the trader's conviction that the theme may be approaching an active move, beyond what any single dimension signals. The dimensions are never combined into a single score or weighted composite; the human trader reads the combination and decides. As of the snapshot, confluence is the overlay of observations in multiple dimensions at the same time."

---

## [performance breadth]
Glossary status: absent
Frequency: 3 across 2 files

Sample usages (up to 5):
1. [CF:L203] — "Performance breadth — what fraction of theme members are participating in the same direction, and whether that fraction is expanding, not the theme's average performance."
2. [CF:L205] — "Breadth combined with low dispersion across members is read as tickers following the same institutional interest, rather than a few names moving independently; high breadth with high dispersion reads differently — some members driven, others dragging."
3. [CUS:L204] — [performance breadth implied in bonding composition breakdown context — US-2.3]

Proposed definition:
The fraction of theme members participating in the same directional move, and whether that fraction is expanding. Assessed in combination with dispersion: high breadth + low dispersion signals shared institutional interest; high breadth + high dispersion signals some members driven while others drag. Breadth is expanding fraction, not average performance. One of four confluence dimensions (CF §2.9); flagged as a working hypothesis not yet empirically validated.

Proposed anti-synonyms: breadth (is a generic market term often understood as measure of market strength and expressed as ratio between advance and decline), average performance, group return, momentum (performance breadth is about the fraction of participating members, not the magnitude of the move)

Confidence: medium
- CF §2.9 defines it clearly. Limited to one file; part of the unvalidated confluence hypothesis.

Open questions:
- Is "performance breadth" the canonical term, or is "breadth" used alone in some contexts? If used alone, could it be confused with market breadth (a broader market concept)?

Trader decision: CONFIRM
Trader notes: "performance breadth" != "breadth" (see anti-synonyms)

---

## [intraday setup density]
Glossary status: absent
Frequency: 2 across 1 file

Sample usages (up to 5):
1. [CF:L196] — "Intraday setup density — the proportion of theme members simultaneously coiling/compressing on the intraday timeframe."
2. [CF:L199] — "Many members of one theme coiling in parallel, while other themes and the broader market do not share that characteristic, is itself a sign of institutional positioning — it says nothing about the direction of the next move, but it puts the trader on alert for what the theme's leaders and laggards do next."

Proposed definition:
The proportion of theme members simultaneously exhibiting coiling or compression behavior on the intraday timeframe, independent of daily-bar sync. A high intraday setup density — relative to other themes and the broader market — is read as a sign of institutional positioning. Direction-neutral: it increases alertness without predicting move direction. One of four confluence dimensions (CF §2.9); flagged as a working hypothesis not yet empirically validated.

Proposed anti-synonyms: density (too broad and generic), volatility, compression level, setup count (intraday setup density is a proportion across members, not a count or a volatility measure)

Confidence: medium
- CF §2.9 is the sole source. Frequency is below the compound noun-phrase threshold of 3 but the concept is load-bearing in §2.9 and is expected to appear in deliverables that cover the confluence hypothesis.

Open questions:
- Does the trader use the full phrase "intraday setup density" or a shorter form ("density," "coiling density")? The full phrase is used in CF §2.9 but may not be the trader's natural vocabulary.
- Should this entry be deferred until §2.9 content is confirmed as validated belief (vs. working hypothesis)?

Trader decision: CONFIRM
Trader notes: "intraday setup density" != "density" (see anti-synonyms)

---

## [narrative formation]
Glossary status: absent
Frequency: 3 across 2 files

Sample usages (up to 5):
1. [CF:L207] — "Narrative formation — a common storyline or topic increasingly surfacing across a group of tickers' company narratives and news coverage, an entirely text-based signal independent of price action in either direction."
2. [CF:L215] — "Narrative formation as a theme-genesis path, not only a confirmation signal. The trader's belief extends beyond using narrative as a fourth confirmation dimension for already-confirmed themes."
3. [FL:L83] — "A common narrative or topic increasingly surfacing across a group of tickers' news and company commentary may itself become the trigger for forming a theme, at the trader's discretion, even before those tickers have crossed a sync threshold..."

Proposed definition:
A common storyline or topic increasingly surfacing across a group of tickers' company narratives and news coverage — a text-based signal entirely independent of price action. Functions in two ways: (a) as the fourth confluence dimension for already-confirmed themes (corroborating that a theme is approaching an active move), and (b) as an alternative theme-genesis path — narrative convergence can lead theme formation before any sync threshold has been crossed, at trader discretion. Per-ticker narrative findings also serve as input to connection investigation generally (FL §1.1).

Proposed anti-synonyms: sentiment (sentiment is directional — positive/negative; narrative formation is about topic convergence, not sentiment), news (news is the raw input; narrative formation is the pattern of convergence across tickers)

Confidence: medium
- CF §2.9 and FL §1.2 are consistent. Flagged as a working hypothesis in CF §2.9.

Open questions:
- Is "narrative formation" the canonical term, or does the trader also use "narrative convergence" (CF §2.9 uses both)? Which is preferred for deliverables?
- Does the narrative-led theme-genesis path (reverse path) have its own term, or is it described only narratively?

Trader decision: REDEFINE
Trader notes: "A common storyline or topic increasingly surfacing across a group of tickers' company narratives and news coverage — a text-based signal entirely independent of price action. Functions in two ways: (a) as the fourth confluence dimension for already-confirmed themes (corroborating that a theme is approaching an active move), and (b) as an alternative theme-genesis path — narrative convergence can constitute a connection between the associated tickers and lead theme formation before any sync threshold has been crossed, at trader discretion. Per-ticker narrative findings also serve as input to connection investigation generally (FL §1.1)."

---
<!-- End of proposals -->
