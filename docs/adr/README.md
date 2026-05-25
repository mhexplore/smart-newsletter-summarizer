# Architecture Decision Records (ADRs)

ADRs capture **why** we made a non-obvious choice. Store them in `docs/adr/` and number sequentially: `0001-title.md`, `0002-title.md`.

## When to write an ADR

- Adding/removing an agent
- Changing pipeline order
- Switching LLM or search provider
- Storing docs or outputs differently

## Template

```markdown
# ADR-NNNN: Title

## Status
Accepted | Superseded by ADR-XXXX

## Context
What problem or constraint led to this decision?

## Decision
What we chose.

## Consequences
Pros, cons, and follow-up work.
```

## Index

| ADR | Title |
|-----|-------|
| [0001](0001-crewai-sequential-pipeline.md) | Sequential Scout → Fact Checker → Editor |
