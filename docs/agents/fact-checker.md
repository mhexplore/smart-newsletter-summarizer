# Fact Checker

## Role

Validate scout output before the Editor writes copy. Reduces broken links and unsupported claims.

## Tools

| Tool | Purpose |
|------|---------|
| Verify All URLs In Text | Batch-check every link in scout report |
| Verify Single URL | Deep-check one suspicious link |
| Tavily News Search | Find corroborating source if original link fails |

## Task

`fact_check_task` — context: `scout_task`

## Expected output

Markdown with:

- Summary counts (reviewed / verified / rejected)
- **Approved for newsletter** — only trusted items
- **Rejected** — with reasons

## Policy

- Broken link + no corroboration → **REJECTED**
- Working link → **VERIFIED**
- Replaced link after Tavily search → **CORROBORATED**

## Implementation

- Config: `config/agents.yaml` → `fact_checker`
- URL logic: `src/tools/url_verify.py`
- Code: `NewsletterCrew.fact_checker()` in `src/crew/newsletter_crew.py`
