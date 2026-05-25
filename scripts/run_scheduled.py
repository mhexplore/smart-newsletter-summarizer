"""
Entry point for GitHub Actions and other schedulers.

Reads NEWSLETTER_TOPIC from the environment, runs the crew, optionally emails.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from src.crew.newsletter_crew import run_newsletter_crew  # noqa: E402
from src.export.email_sender import send_newsletter_email  # noqa: E402


def main() -> None:
    topic = os.getenv("NEWSLETTER_TOPIC", "latest developments in AI agents")
    send_email = os.getenv("SEND_EMAIL", "false").lower() in ("1", "true", "yes")
    dry_run = os.getenv("EMAIL_DRY_RUN", "false").lower() in ("1", "true", "yes")

    print(f"Topic: {topic}")
    output = run_newsletter_crew(topic)
    print(output)

    newsletter_path = ROOT / "output" / "newsletter.md"
    if send_email:
        result = send_newsletter_email(newsletter_path, dry_run=dry_run)
        print(f"Email: {result['status']} → {result['recipients']} ({result['subject']})")
    else:
        print("Email skipped (set SEND_EMAIL=true to send).")


if __name__ == "__main__":
    main()
