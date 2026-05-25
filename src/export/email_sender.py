"""
Send the generated newsletter via SMTP (Gmail, Outlook, SendGrid SMTP, etc.).
"""

from __future__ import annotations

import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

try:
    import markdown as md_lib
except ImportError:  # pragma: no cover
    md_lib = None


def _markdown_to_html(body: str) -> str:
    if md_lib:
        return md_lib.markdown(body, extensions=["extra", "sane_lists"])
    escaped = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"<pre style='font-family:sans-serif'>{escaped}</pre>"


def _extract_subject(newsletter_md: str, fallback: str) -> str:
    """Use first markdown H1 or a 'Subject line:' prefix if present."""
    for line in newsletter_md.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("subject line:"):
            return stripped.split(":", 1)[1].strip()[:120]
        if stripped.startswith("# "):
            return stripped[2:].strip()[:120]
    match = re.search(r"^Subject:\s*(.+)$", newsletter_md, re.MULTILINE | re.IGNORECASE)
    if match:
        return match.group(1).strip()[:120]
    return fallback[:120]


def send_newsletter_email(
    newsletter_path: Path | str,
    *,
    subject: str | None = None,
    to_addresses: str | list[str] | None = None,
    dry_run: bool = False,
) -> dict[str, str]:
    """
    Send newsletter Markdown as multipart (plain + HTML) email.

    Required env vars:
        SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM

    Optional:
        EMAIL_TO (comma-separated) — overridden by to_addresses

    Returns:
        dict with status, subject, recipients
    """
    path = Path(newsletter_path)
    if not path.exists():
        raise FileNotFoundError(f"Newsletter file not found: {path}")

    body_md = path.read_text(encoding="utf-8")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM") or smtp_user

    raw_to = to_addresses or os.getenv("EMAIL_TO", "")
    if isinstance(raw_to, str):
        recipients = [a.strip() for a in raw_to.split(",") if a.strip()]
    else:
        recipients = list(raw_to)

    if not all([smtp_host, smtp_user, smtp_password, email_from, recipients]):
        raise EnvironmentError(
            "Email requires SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, "
            "EMAIL_FROM, and EMAIL_TO (or to_addresses)."
        )

    topic_fallback = os.getenv("NEWSLETTER_TOPIC", "Smart Newsletter")
    email_subject = subject or _extract_subject(body_md, f"{topic_fallback} — Weekly Digest")
    html_body = _markdown_to_html(body_md)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = email_subject
    msg["From"] = email_from
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(body_md, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    if dry_run:
        return {
            "status": "dry_run",
            "subject": email_subject,
            "recipients": ", ".join(recipients),
        }

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_from, recipients, msg.as_string())

    return {
        "status": "sent",
        "subject": email_subject,
        "recipients": ", ".join(recipients),
    }
