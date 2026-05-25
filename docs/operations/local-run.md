# Local run

## Prerequisites

- Python **3.11** (system default or project `.venv`)
- `.env` from `.env.example`

On Windows, set the system default once:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.cursor\skills\python-upgrade\scripts\configure_system_python.ps1" -TargetVersion 3.11
```

Then restart the terminal.

## Install

```powershell
cd smart-newsletter-summarizer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

## Commands

| Command | Description |
|---------|-------------|
| `python main.py --test-tools` | RSS + Tavily + URL verify (no LLM) |
| `python main.py --topic "AI agents"` | Full crew |
| `python main.py --topic "https://hnrss.org/frontpage"` | RSS mode |
| `python main.py --topic "AI" --email` | Crew + SMTP send |
| `python main.py --email-only` | Send existing `output/newsletter.md` |
| `python main.py --email-only --email-dry-run` | Validate SMTP config |

## Outputs

Check `output/` after a full run:

- `scout_report.md`
- `fact_check_report.md`
- `newsletter.md`

## Scheduler script (same as CI)

```powershell
$env:NEWSLETTER_TOPIC = "generative AI news"
$env:SEND_EMAIL = "false"
python scripts/run_scheduled.py
```
