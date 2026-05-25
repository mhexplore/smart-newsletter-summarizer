"""
URL verification helpers for the fact-checker agent.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

import requests

_URL_PATTERN = re.compile(r"https?://[^\s\)\]>\"']+", re.IGNORECASE)


def extract_urls(text: str) -> list[str]:
    """Pull HTTP(S) URLs from free-form agent text."""
    return list(dict.fromkeys(_URL_PATTERN.findall(text)))


def verify_url(url: str, timeout: int = 10) -> dict[str, Any]:
    """
    Check whether a URL is reachable (HEAD, then GET fallback).

    Returns:
        dict with keys: url, ok, status_code, final_url, error
    """
    if not url or not url.strip():
        raise ValueError("url must be non-empty")

    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError("url must use http or https")

    result: dict[str, Any] = {
        "url": url.strip(),
        "ok": False,
        "status_code": None,
        "final_url": None,
        "error": None,
    }

    headers = {"User-Agent": "SmartNewsletterSummarizer/1.0 (fact-checker)"}

    try:
        response = requests.head(
            result["url"],
            allow_redirects=True,
            timeout=timeout,
            headers=headers,
        )
        if response.status_code >= 400 or response.status_code in (405, 501):
            response = requests.get(
                result["url"],
                allow_redirects=True,
                timeout=timeout,
                headers=headers,
                stream=True,
            )
            response.close()

        result["status_code"] = response.status_code
        result["final_url"] = str(response.url)
        result["ok"] = 200 <= response.status_code < 400
    except requests.RequestException as exc:
        result["error"] = str(exc)

    return result


def verify_urls_in_text(text: str, max_urls: int = 15) -> str:
    """Verify all URLs found in text; return a human-readable report."""
    urls = extract_urls(text)[:max_urls]
    if not urls:
        return "No URLs found to verify."

    lines: list[str] = []
    for url in urls:
        check = verify_url(url)
        status = check.get("status_code", "n/a")
        if check["ok"]:
            lines.append(f"OK ({status}): {url}")
        else:
            err = check.get("error") or f"HTTP {status}"
            lines.append(f"FAILED ({err}): {url}")

    return "\n".join(lines)
