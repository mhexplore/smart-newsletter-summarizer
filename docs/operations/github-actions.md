# GitHub Actions

Workflow file: `.github/workflows/newsletter.yml`

## Triggers

| Trigger | When |
|---------|------|
| `schedule` | Mondays 08:00 UTC (`0 8 * * 1`) |
| `workflow_dispatch` | Manual run from Actions tab |

## Manual run

1. GitHub → **Actions** → **Smart Newsletter** → **Run workflow**
2. Set **topic** (optional)
3. Toggle **send_email** if SMTP secrets are configured

## Repository configuration

### Secrets (Settings → Secrets and variables → Actions)

| Secret | Required |
|--------|----------|
| `OPENAI_API_KEY` | Yes |
| `TAVILY_API_KEY` | Recommended for keyword topics |
| `SMTP_HOST` | Only if emailing |
| `SMTP_PORT` | Only if emailing |
| `SMTP_USER` | Only if emailing |
| `SMTP_PASSWORD` | Only if emailing |
| `EMAIL_FROM` | Only if emailing |
| `EMAIL_TO` | Only if emailing |

### Variables (optional)

| Variable | Example | Purpose |
|----------|---------|---------|
| `NEWSLETTER_TOPIC` | `AI agents weekly` | Default topic on schedule |
| `SEND_EMAIL` | `true` | Email after every scheduled run |

## Artifacts

Each run uploads:

- `newsletter.md`
- `scout_report.md`
- `fact_check_report.md`

Retention: 90 days. Download from the workflow run page.

## Customize schedule

Edit the `cron` line in `newsletter.yml`. [crontab.guru](https://crontab.guru/) helps build expressions.

Example — Fridays 7am US Eastern (approx. `0 12 * * 5` UTC in winter; adjust for DST):

```yaml
- cron: "0 12 * * 5"
```

## Entry point

CI runs `python scripts/run_scheduled.py`, which respects:

- `NEWSLETTER_TOPIC`
- `SEND_EMAIL`
- All SMTP secrets when sending
