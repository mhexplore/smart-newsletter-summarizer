"""
CrewAI tool wrappers around news_sources.py and url_verify.py.
"""

from crewai.tools import tool

from src.tools.news_sources import (
    fetch_rss_feed,
    format_articles_for_agent,
    search_news_tavily,
)
from src.tools.url_verify import verify_url, verify_urls_in_text


@tool("RSS Feed Reader")
def rss_feed_reader(feed_url: str, max_entries: int = 8) -> str:
    """
    Fetch recent articles from an RSS or Atom feed URL.
    Use this for known newsletter or news site feeds (e.g. TechCrunch, Hacker News).

    Args:
        feed_url: Full RSS/Atom feed URL.
        max_entries: How many recent articles to fetch (default 8).
    """
    articles = fetch_rss_feed(feed_url=feed_url, max_entries=max_entries)
    return format_articles_for_agent(articles)


@tool("Tavily News Search")
def tavily_news_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for recent news on a topic using Tavily AI.
    Use this when you need to discover stories by keyword rather than a fixed RSS URL.

    Args:
        query: What to search for (e.g. "generative AI product launches May 2026").
        max_results: Number of results (1–10, default 5).
    """
    articles = search_news_tavily(query=query, max_results=max_results)
    return format_articles_for_agent(articles)


@tool("Verify Single URL")
def verify_single_url(url: str) -> str:
    """
    Check if a single article link is reachable (HTTP status, redirects).
    Use before approving a story for the newsletter.

    Args:
        url: Full HTTP or HTTPS URL to verify.
    """
    check = verify_url(url)
    if check["ok"]:
        return f"VERIFIED: {url} (status {check['status_code']}, final URL: {check['final_url']})"
    err = check.get("error") or f"status {check.get('status_code')}"
    return f"UNVERIFIED: {url} — {err}"


@tool("Verify All URLs In Text")
def verify_all_urls_in_text(text: str) -> str:
    """
    Extract and verify every HTTP(S) URL in a block of text (scout report or draft).
    Returns a line-by-line pass/fail report.

    Args:
        text: Any text containing article links (scout output, draft newsletter, etc.).
    """
    return verify_urls_in_text(text)
