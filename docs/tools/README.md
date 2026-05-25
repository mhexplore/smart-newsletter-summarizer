# Tools catalog

CrewAI agents call **tools** (`@tool` in `src/tools/crew_tools.py`). Implementation lives in plain Python modules.

## News ingestion

| Tool | Module | Function |
|------|--------|----------|
| RSS Feed Reader | `news_sources.py` | `fetch_rss_feed()` |
| Tavily News Search | `news_sources.py` | `search_news_tavily()` |

## Verification

| Tool | Module | Function |
|------|--------|----------|
| Verify Single URL | `url_verify.py` | `verify_url()` |
| Verify All URLs In Text | `url_verify.py` | `verify_urls_in_text()` |

## Agent → tool mapping

| Agent | Tools |
|-------|-------|
| News Scout | RSS Feed Reader, Tavily News Search |
| Fact Checker | Verify Single URL, Verify All URLs In Text, Tavily News Search |
| Summarizer | — |

## Adding a new tool

1. Implement logic in `src/tools/<module>.py`
2. Add `@tool` wrapper in `crew_tools.py`
3. Assign to agent(s) in `newsletter_crew.py`
4. Document here and mention in task YAML if needed
