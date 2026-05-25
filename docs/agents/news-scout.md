# News Scout

## Role

Discover recent articles for the given `{topic}` using external data only (no invention).

## Tools

| Tool | When to use |
|------|-------------|
| RSS Feed Reader | `topic` is an `http(s)` URL |
| Tavily News Search | `topic` is keywords |

## Task

`scout_task` in `config/tasks.yaml`

## Expected output

Bullet list: title, link, one-sentence summary per article.

## Implementation

- Config: `config/agents.yaml` → `news_scout`
- Code: `NewsletterCrew.news_scout()` in `src/crew/newsletter_crew.py`
