# ADR-0001: Sequential Scout → Fact Checker → Editor pipeline

## Status

Accepted

## Context

Early versions ran Scout → Editor only. LLMs sometimes summarized broken links or exaggerated headlines. We needed lightweight verification without a separate microservice.

## Decision

1. Insert a **Fact Checker** agent between Scout and Editor.
2. Use **CrewAI `Process.sequential`** — no parallel fan-out.
3. Give Fact Checker **URL verification tools** plus Tavily for corroboration.
4. Editor task context = fact-check output only (not raw scout list).
5. Persist three Markdown artifacts per run for audit.

## Consequences

**Pros**

- Clear handoffs and debuggable intermediate files
- Editors cannot easily bypass rejected stories
- Fits GitHub Actions (single job, linear steps)

**Cons**

- Higher latency and token cost (third agent pass)
- Fact checking is heuristic (HTTP + search), not legal-grade verification

**Follow-up**

- Optional fourth agent for tone/style QA
- Cache Tavily results per topic to reduce API calls
