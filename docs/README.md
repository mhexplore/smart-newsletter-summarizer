# Technical documentation

Documentation for the Smart Newsletter Summarizer agent system. Store and version this folder **in GitHub** alongside code so humans and AI assistants share one source of truth.

## Recommended layout

```
docs/
├── README.md                 ← You are here (index)
├── architecture/
│   ├── overview.md           ← System context & components
│   └── data-flow.md          ← Inputs, outputs, artifacts
├── agents/
│   ├── README.md             ← Agent roster
│   ├── news-scout.md
│   ├── fact-checker.md
│   └── summarizer.md
├── tools/
│   └── README.md             ← Tool catalog
├── operations/
│   ├── local-run.md
│   ├── github-actions.md
│   ├── email-delivery.md
│   └── secrets.md
└── adr/
    ├── README.md             ← When to write an ADR
    └── 0001-crewai-sequential-pipeline.md
```

## For AI assistants

Root **[AGENTS.md](../AGENTS.md)** is the fast entry point. Point Cursor at:

`https://github.com/YOUR_USERNAME/smart-newsletter-summarizer/blob/main/AGENTS.md`

## Maintenance rules

1. **Code change → doc change** — new agent, tool, or env var updates the matching doc in the same PR.
2. **Architecture** — update Mermaid diagrams in `architecture/` when the pipeline changes.
3. **ADRs** — use `docs/adr/` for non-obvious decisions (e.g. why Fact Checker runs before Editor).
4. **Generated artifacts** — `output/*.md` are runtime outputs, not documentation.

## Quick links

- [Architecture overview](architecture/overview.md)
- [Data flow & artifacts](architecture/data-flow.md)
- [Agents](agents/README.md)
- [Tools](tools/README.md)
- [Local run](operations/local-run.md)
- [GitHub Actions](operations/github-actions.md)
- [Email delivery](operations/email-delivery.md)
- [Secrets](operations/secrets.md)
