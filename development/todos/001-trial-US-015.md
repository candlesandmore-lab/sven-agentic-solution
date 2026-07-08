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

>> refinement prompt:

There are no precomputed narrative findings, part of this todo success criteria is to implement an agentic workflow that extracts narratives from the above mentioned sources via FMP data provider (we have the API access).