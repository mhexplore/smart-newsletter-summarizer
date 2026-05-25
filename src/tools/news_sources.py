"""
Plain Python functions for fetching news from RSS feeds and Tavily search.
These are wrapped as CrewAI tools in crew_tools.py.
"""

from __future__ import annotations

import os
from typing import Any

import feedparser
import requests


def fetch_rss_feed(feed_url: str, max_entries: int = 10) -> list[dict[str, Any]]:
    """
    Scrape an RSS or Atom feed and return recent articles.

    Args:
        feed_url: Full URL of the RSS/Atom feed.
        max_entries: Maximum number of entries to return (newest first).

    Returns:
        List of dicts with keys: title, link, summary, published.

    Raises:
        ValueError: If the feed URL is empty or the feed cannot be parsed.
    """
    if not feed_url or not feed_url.strip():
        raise ValueError("feed_url must be a non-empty string")

    parsed = feedparser.parse(feed_url.strip())

    if getattr(parsed, "bozo", False) and not parsed.entries:
        exc = getattr(parsed, "bozo_exception", None)
        raise ValueError(f"Failed to parse feed: {exc}")

    feed_title = parsed.feed.get("title", "Unknown feed")
    articles: list[dict[str, Any]] = []

    for entry in parsed.entries[:max_entries]:
        summary = entry.get("summary") or entry.get("description") or ""
        # Strip basic HTML tags from summaries when present
        if "<" in summary:
            import re

            summary = re.sub(r"<[^>]+>", "", summary).strip()

        articles.append(
            {
                "feed": feed_title,
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "summary": summary[:500] if summary else "",
                "published": entry.get("published") or entry.get("updated", ""),
            }
        )

    return articles


def search_news_tavily(
    query: str,
    max_results: int = 5,
    api_key: str | None = None,
) -> list[dict[str, Any]]:
    """
    Search the web for recent news using the Tavily API (free tier available).

    Sign up at https://tavily.com and set TAVILY_API_KEY in your .env file.

    Args:
        query: Search query (e.g. "AI newsletter trends this week").
        max_results: Number of results to return (1–10).
        api_key: Tavily API key; defaults to TAVILY_API_KEY env var.

    Returns:
        List of dicts with keys: title, url, content, score.

    Raises:
        ValueError: If query is empty or API key is missing.
        requests.HTTPError: If the Tavily API returns an error.
    """
    if not query or not query.strip():
        raise ValueError("query must be a non-empty string")

    key = api_key or os.getenv("TAVILY_API_KEY")
    if not key:
        raise ValueError(
            "TAVILY_API_KEY is not set. Set it in your environment or .env file "
            "(local), or as a GitHub Actions repository secret (cloud). "
            "Get a free key at https://tavily.com"
        )

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": key,
            "query": query.strip(),
            "search_depth": "basic",
            "topic": "news",
            "max_results": min(max(max_results, 1), 10),
            "include_answer": False,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    results: list[dict[str, Any]] = []
    for item in data.get("results", []):
        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": (item.get("content") or "")[:600],
                "score": item.get("score"),
            }
        )

    return results


def format_articles_for_agent(articles: list[dict[str, Any]]) -> str:
    """Turn article dicts into readable text for the LLM."""
    if not articles:
        return "No articles found."

    lines: list[str] = []
    for i, article in enumerate(articles, start=1):
        title = article.get("title", "Untitled")
        link = article.get("url") or article.get("link", "")
        summary = article.get("content") or article.get("summary", "")
        published = article.get("published", "")
        feed = article.get("feed", "")

        block = f"{i}. **{title}**"
        if feed:
            block += f" ({feed})"
        if published:
            block += f"\n   Published: {published}"
        if link:
            block += f"\n   Link: {link}"
        if summary:
            block += f"\n   Summary: {summary}"
        lines.append(block)

    return "\n\n".join(lines)
