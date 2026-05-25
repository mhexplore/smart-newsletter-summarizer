# AGENTS.md — Guide for AI coding assistants

This file helps Cursor, Copilot, and other agents navigate and extend this repository.

## What this project does

A **CrewAI** pipeline that:

1. **News Scout** — fetches articles (RSS or Tavily search)
2. **Fact Checker** — verifies URLs and corroborates claims
3. **Newsletter Editor** — writes `output/newsletter.md`
4. **Email export** (optional) — SMTP delivery
5. **GitHub Actions** — scheduled or manual runs

LLM: `gpt-4o-mini` (all agents).

## Start here

| Goal | Read first |
|------|------------|
| Architecture | [docs/architecture/overview.md](docs/architecture/overview.md) |
| Change an agent | [docs/agents/README.md](docs/agents/README.md) + `config/agents.yaml` |
| Add a tool | [docs/tools/README.md](docs/tools/README.md) + `src/tools/` |
| Run locally | [docs/operations/local-run.md](docs/operations/local-run.md) |
| CI / schedule | [docs/operations/github-actions.md](docs/operations/github-actions.md) |
| Email | [docs/operations/email-delivery.md](docs/operations/email-delivery.md) |

## Key files (do not duplicate logic elsewhere)

```
config/agents.yaml          # Agent personas
config/tasks.yaml           # Task prompts & expected outputs
src/tools/news_sources.py   # RSS + Tavily (plain Python)
src/tools/url_verify.py     # URL reachability checks
src/tools/crew_tools.py     # @tool wrappers for CrewAI
src/crew/newsletter_crew.py # Agent/task wiring
src/export/email_sender.py  # SMTP send
scripts/run_scheduled.py    # CI entry point
.github/workflows/newsletter.yml
```

## Conventions

- New tools: implement in `src/tools/<name>.py`, wrap in `crew_tools.py` with `@tool`.
- New agents: add to `config/agents.yaml` + `config/tasks.yaml`, then methods in `newsletter_crew.py`.
- Task order is **sequential**: scout → fact_check → summarize.
- Outputs go under `output/` (gitignored except `.gitkeep`).
- Documentation lives in `docs/`; update architecture diagram when flow changes.

## Safe changes

- Adjust prompts in YAML without touching Python.
- Add env vars to `.env.example` and `docs/operations/secrets.md`.
- Never commit `.env` or API keys.

## Testing without LLM cost

```bash
python main.py --test-tools
```

## Full crew + email

```bash
python main.py --topic "AI agents" --email
```
