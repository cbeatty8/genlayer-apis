"""
Generic web fetching and scraping helpers for GenLayer Intelligent Contracts.

Uses gl.get_from_web() under the hood.
"""

import json
import re
import genlayer.gl as gl


def fetch_json(url: str) -> dict | list:
    """
    Fetch and parse JSON from a URL.

    :param url: URL to fetch
    :returns: Parsed JSON (dict or list)

    Example::

        data = fetch_json("https://api.example.com/prices")
    """
    response = gl.get_from_web(url=url, mode="raw")
    return json.loads(response)


def fetch_text(url: str) -> str:
    """
    Fetch raw text/HTML from a URL.

    :param url: URL to fetch
    :returns: Raw text content

    Example::

        html = fetch_text("https://example.com")
    """
    return gl.get_from_web(url=url, mode="raw")


def scrape_links(url: str, filter_pattern: str = "") -> list[str]:
    """
    Extract all links from an HTML page.

    :param url: URL to scrape
    :param filter_pattern: Optional regex pattern to filter links (e.g. "github.com")
    :returns: List of URLs found in href attributes

    Example::

        links = scrape_links("https://news.ycombinator.com", filter_pattern="github.com")
    """
    html = fetch_text(url)

    # Simple regex for href extraction
    href_pattern = r'href=["\']([^"\']+)["\']'
    matches = re.findall(href_pattern, html)

    if filter_pattern:
        matches = [link for link in matches if re.search(filter_pattern, link)]

    return matches


def scrape_text(url: str, tag: str = "body") -> str:
    """
    Extract text content from an HTML element.

    :param url: URL to scrape
    :param tag: HTML tag to extract text from (default "body")
    :returns: Text content with HTML tags removed

    Example::

        text = scrape_text("https://example.com", tag="p")
    """
    html = fetch_text(url)

    # Extract content between tags
    tag_pattern = rf'<{tag}[^>]*>(.*?)</{tag}>'
    matches = re.findall(tag_pattern, html, re.DOTALL | re.IGNORECASE)

    if not matches:
        return ""

    # Remove HTML tags
    content = "\n".join(matches)
    clean = re.sub(r'<[^>]+>', ' ', content)
    clean = re.sub(r'\s+', ' ', clean).strip()

    return clean
