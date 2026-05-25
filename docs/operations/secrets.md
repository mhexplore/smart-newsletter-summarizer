# Secrets & environment variables

Never commit `.env`. Use this table as the canonical reference.

## Local (`.env`)

| Variable | Required | Used by |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | All agents |
| `TAVILY_API_KEY` | For keyword search | Scout, Fact Checker |
| `NEWSLETTER_TOPIC` | No | CLI / scheduler default |
| `SMTP_HOST` | For email | `email_sender.py` |
| `SMTP_PORT` | For email | Usually `587` |
| `SMTP_USER` | For email | SMTP auth |
| `SMTP_PASSWORD` | For email | SMTP auth |
| `EMAIL_FROM` | For email | Defaults to `SMTP_USER` |
| `EMAIL_TO` | For email | Comma-separated recipients |
| `SEND_EMAIL` | No | `scripts/run_scheduled.py` |
| `EMAIL_DRY_RUN` | No | Validate without sending |

## GitHub Actions

Copy the same names into **Repository secrets**. Optional **Variables**:

- `NEWSLETTER_TOPIC`
- `SEND_EMAIL`

## Rotation

1. Revoke old key at provider (OpenAI, Tavily, Google app password)
2. Update `.env` and GitHub Secrets
3. Re-run workflow to confirm

## Cost controls

- Use `--test-tools` before full runs
- Lower frequency in `newsletter.yml` cron
- Keep `gpt-4o-mini` (already configured)
