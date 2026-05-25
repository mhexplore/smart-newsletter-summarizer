# Email delivery

Module: `src/export/email_sender.py`

## How it works

1. Reads `output/newsletter.md`
2. Extracts subject from `Subject line:` or first `#` heading
3. Converts Markdown to HTML (`markdown` package)
4. Sends multipart email via SMTP + STARTTLS

## Gmail setup

1. Enable 2FA on your Google account
2. Create an **App Password**: Google Account → Security → App passwords
3. Set in `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_FROM=you@gmail.com
EMAIL_TO=subscriber@example.com
```

## CLI

```powershell
# Generate then send
python main.py --topic "AI news" --email

# Send last newsletter only
python main.py --email-only

# Test config without sending
python main.py --email-only --email-dry-run
```

## GitHub Actions

Set SMTP secrets (see [secrets.md](secrets.md)), then either:

- Enable **send_email** on manual workflow dispatch, or
- Set repository variable `SEND_EMAIL=true` for scheduled runs

## Troubleshooting

| Error | Fix |
|-------|-----|
| `Email requires SMTP_*` | Fill all SMTP vars in `.env` or GitHub Secrets |
| Authentication failed | Use app password, not account password (Gmail) |
| Empty body | Ensure `output/newsletter.md` exists from a prior crew run |
