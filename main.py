"""
Smart Newsletter Summarizer — entry point.

Examples:
  python main.py --topic "open source AI agents"
  python main.py --topic "https://hnrss.org/frontpage" --email
  python main.py --test-tools
  python main.py --email-only
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
NEWSLETTER_PATH = ROOT / "output" / "newsletter.md"


def test_tools() -> None:
    """Quick check that RSS, Tavily, and URL verify work without the LLM."""
    from src.tools.news_sources import (
        fetch_rss_feed,
        format_articles_for_agent,
        search_news_tavily,
    )
    from src.tools.url_verify import verify_url

    print("=== RSS test (Hacker News front page) ===\n")
    articles = fetch_rss_feed("https://hnrss.org/frontpage", max_entries=3)
    print(format_articles_for_agent(articles))

    print("\n=== Tavily test (skipped if no API key) ===\n")
    try:
        results = search_news_tavily("AI agents news", max_results=3)
        print(format_articles_for_agent(results))
    except ValueError as e:
        print(f"Tavily skipped: {e}")

    print("\n=== URL verify test ===\n")
    check = verify_url("https://hnrss.org/frontpage")
    print(check)


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart Newsletter Summarizer")
    parser.add_argument(
        "--topic",
        type=str,
        default=os.getenv("NEWSLETTER_TOPIC", "latest developments in AI agents"),
        help="Search topic OR an RSS feed URL",
    )
    parser.add_argument(
        "--test-tools",
        action="store_true",
        help="Test RSS/Tavily/URL verify only (no OpenAI cost)",
    )
    parser.add_argument(
        "--email",
        action="store_true",
        help="Send output/newsletter.md via SMTP after the crew finishes",
    )
    parser.add_argument(
        "--email-only",
        action="store_true",
        help="Send existing output/newsletter.md without running the crew",
    )
    parser.add_argument(
        "--email-dry-run",
        action="store_true",
        help="Validate email config without sending",
    )
    args = parser.parse_args()

    if args.test_tools:
        test_tools()
        return

    if args.email_only:
        from src.export.email_sender import send_newsletter_email

        result = send_newsletter_email(
            NEWSLETTER_PATH,
            dry_run=args.email_dry_run,
        )
        print(f"Email {result['status']}: {result['subject']} → {result['recipients']}")
        return

    from src.crew.newsletter_crew import run_newsletter_crew

    print(
        f"Running News Scout → Fact Checker → Editor for: {args.topic}\n"
    )
    output = run_newsletter_crew(args.topic)
    print("\n=== NEWSLETTER ===\n")
    print(output)

    if args.email:
        from src.export.email_sender import send_newsletter_email

        result = send_newsletter_email(
            NEWSLETTER_PATH,
            dry_run=args.email_dry_run,
        )
        print(
            f"\nEmail {result['status']}: {result['subject']} → {result['recipients']}"
        )


if __name__ == "__main__":
    main()
