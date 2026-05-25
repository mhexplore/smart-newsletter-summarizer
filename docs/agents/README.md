# Agents

Three CrewAI agents run **sequentially**. Definitions live in `config/agents.yaml`; behavior is shaped by `config/tasks.yaml`.

| Agent | Tools | Output artifact |
|-------|-------|-----------------|
| [News Scout](news-scout.md) | RSS, Tavily | `scout_report.md` |
| [Fact Checker](fact-checker.md) | URL verify, Tavily | `fact_check_report.md` |
| [Summarizer](summarizer.md) | none | `newsletter.md` |

LLM for all agents: `gpt-4o-mini` (set in `src/crew/newsletter_crew.py`).

## Adding a fourth agent

1. Add persona to `config/agents.yaml`
2. Add task to `config/tasks.yaml` with `context` pointing to prior task
3. Add `@agent` and `@task` methods in `newsletter_crew.py`
4. Document in `docs/agents/<name>.md` and update architecture diagrams
