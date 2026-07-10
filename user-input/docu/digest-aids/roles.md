# Roles — Agent-Build-Agents Input Corpus
v0.3 — 2026-07-06

<scope>
This document enumerates the actors that appear inside the four input documents
(market behaviors, trading strategies, user stories, tech-stack constraints) and
their digest aids. Roles used only in the authoring process (Claude, the user
orchestrating the authoring, adversarial reviewer personas) are out of scope
here and belong to the handbook.

Actor modeling in this corpus is deliberately at the interaction boundary.
What happens *inside* the Technical Trader Solution's boundary — whether a given capability
is implemented as a deterministic algorithm, an LLM call, an agent, or a REST
call to an external service — is not a role and is not modeled here. Those are
implementation choices the client agent-build-agents project makes.
</scope>

## Roles present in the corpus

### Human trader

<definition>
The single human domain expert whose knowledge, observations, and interaction
requirements are the source material for the entire corpus. Sole human actor
referenced anywhere in the deliverables. Appears explicitly in user stories.
</definition>

<rule strictness="hard">
The bare word "trader" must never appear in any deliverable doc. Always
"human trader".
</rule>

### Technical Trader Solution

<definition>
The complete delivered artifact — the union of interface, data integrations,
deterministic components, and any internal AI-based components the client
project chooses to include. The human trader interacts with the Technical Trader
Solution; what the Technical Trader Solution uses internally is implementation, not role.
</definition>

<rule strictness="hard">
The bare words "Technical", "Trader" (when standing in for this role), and
"Solution" must not appear individually where "Technical Trader Solution" is
meant. Partial forms "Technical Trader" and "Trader Solution" are also
prohibited. Always use the full three-word form. The retired name "cockpit
system" and bare "cockpit" are additionally prohibited. File-path and
identifier references (e.g. the snapshot filename `cockpit-user-stories.md`)
are excluded from this rule.
</rule>

## Roles explicitly excluded

<out-of-scope>
### Agent / Runtime agent / AI / LLM (as roles)
No AI-based construct is a role in this corpus. Any AI functionality lives
inside the Technical Trader Solution's boundary as an implementation choice. The client
agent-build-agents project decides whether and where to use agents, LLMs, or
purely deterministic code. Elevating any of these to actor status pre-decides
implementation and is prohibited.
</out-of-scope>

<out-of-scope>
### Agent trader
No agent operates autonomously as a trader anywhere in this corpus. Named
here only to prevent readers from inferring an agent-trader role from context.
</out-of-scope>

<out-of-scope>
### Build-time agents
The client agent-build-agents project's internal agent constellation (planner,
coder, reviewer, etc.) exists only during Technical Trader Solution construction. It is a
concern of the client project, not of our deliverables. Never referenced in
the corpus.
</out-of-scope>

<out-of-scope>
### Claude / authoring user
Actors of the authoring process. Never referenced in any deliverable doc.
Their behavior is documented in the handbook and skills, not in the corpus.
</out-of-scope>

## Technology language in the corpus

<rule strictness="hard">
Technology terms (agent, LLM, AI, API, database, service, framework, model
in its ML sense, etc.) do not appear as actor references anywhere in the
corpus. They may appear in the tech-stack constraints doc (that is its
purpose) and in non-functional requirements within user stories (response
time, cost, visual choices, etc.). Everywhere else — market-behavior content,
trading-strategy content, user-story functional content — technology terms
are prohibited. See glossary "tech-restricted" category and the
user-story-authoring skill (Batch 2) for the doc-specific rule.
</rule>

## Role presence by document

| Document | Roles present |
|---|---|
| Market behaviors | none (role-agnostic; descriptive of market phenomena) |
| Trading strategies | none (role-agnostic; describes strategy mechanics) |
| User stories | human trader, Technical Trader Solution |
| Tech-stack constraints | Technical Trader Solution |

## Change log

- v0.3 (2026-07-06) — renamed role "Cockpit system" → "Technical Trader Solution"
  (client-project feedback: receiving agents confused by "cockpit"); updated
  prohibition rule (bare "Solution", partial forms "Technical Trader" / "Trader
  Solution", retired "cockpit system" / bare "cockpit" all prohibited); updated
  all active-content references; changelog entries preserved as historical record.
- v0.2 (2026-07-03) — removed Runtime agent role per modeling review (AI is
  implementation inside the cockpit system's boundary, not an actor); renamed
  System → Cockpit system; added corpus-level technology-language rule;
  extended bare-word rule to cover bare "cockpit" (not just bare "system")
  and reworded Cockpit-system definition to avoid bare "cockpit" itself.
- v0.1 (2026-07-02) — initial draft.
