"""
News and RSS feed helpers for GenLayer Intelligent Contracts.

Fetch news from RSS feeds and Hacker News. No API key required.
"""

import json
import re
import genlayer.gl as gl


def fetch_rss(url: str, max_items: int = 10) -> list[dict]:
    """
    Fetch and parse an RSS/Atom feed.

    :param url: RSS/Atom feed URL
    :param max_items: Maximum number of items to return (default 10)
    :returns: List of dicts with keys: title, link, description, published

    Example::

        news = fetch_rss("https://feeds.bbci.co.uk/news/rss.xml", max_items=5)
        # [{'title': 'Breaking News...', 'link': 'https://...', ...}, ...]
    """
    xml_text = gl.get_from_web(url=url, mode="raw")

    items = []

    # Parse RSS items
    item_pattern = r'<item[^>]*>(.*?)</item>'
    for match in re.finditer(item_pattern, xml_text, re.DOTALL):
        item_xml = match.group(1)
        item = _parse_rss_item(item_xml)
        if item:
            items.append(item)
        if len(items) >= max_items:
            break

    # Parse Atom entries if no RSS items found
    if not items:
        entry_pattern = r'<entry[^>]*>(.*?)</entry>'
        for match in re.finditer(entry_pattern, xml_text, re.DOTALL):
            entry_xml = match.group(1)
            item = _parse_atom_entry(entry_xml)
            if item:
                items.append(item)
            if len(items) >= max_items:
                break

    return items


def _parse_rss_item(xml: str) -> dict | None:
    """Parse a single RSS <item> element."""
    title = _extract_tag(xml, "title")
    if not title:
        return None

    return {
        "title": _clean_text(title),
        "link": _extract_tag(xml, "link") or "",
        "description": _clean_text(_extract_tag(xml, "description") or ""),
        "published": _extract_tag(xml, "pubDate") or "",
    }


def _parse_atom_entry(xml: str) -> dict | None:
    """Parse a single Atom <entry> element."""
    title = _extract_tag(xml, "title")
    if not title:
        return None

    # Atom links use href attribute
    link_match = re.search(r'<link[^>]*href=["\']([^"\']+)["\']', xml)
    link = link_match.group(1) if link_match else ""

    return {
        "title": _clean_text(title),
        "link": link,
        "description": _clean_text(_extract_tag(xml, "summary") or ""),
        "published": _extract_tag(xml, "published") or _extract_tag(xml, "updated") or "",
    }


def _extract_tag(xml: str, tag: str) -> str | None:
    """Extract text content from an XML tag."""
    match = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', xml, re.DOTALL)
    return match.group(1).strip() if match else None


def _clean_text(text: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def hackernews_top(max_items: int = 10) -> list[dict]:
    """
    Fetch top stories from Hacker News.

    :param max_items: Maximum number of stories to return (default 10)
    :returns: List of dicts with keys: title, url, score, author, comments

    Example::

        top = hackernews_top(max_items=5)
        # [{'title': 'Show HN: ...', 'url': 'https://...', 'score': 250, ...}, ...]
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = gl.get_from_web(url=url, mode="raw")
    story_ids = json.loads(response)[:max_items]

    stories = []
    for sid in story_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
        item_response = gl.get_from_web(url=item_url, mode="raw")
        item = json.loads(item_response)

        stories.append({
            "title": item.get("title", ""),
            "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
            "score": item.get("score", 0),
            "author": item.get("by", ""),
            "comments": item.get("descendants", 0),
        })

    return stories


def search_hackernews(query: str, max_items: int = 10) -> list[dict]:
    """
    Search Hacker News stories.

    :param query: Search query
    :param max_items: Maximum number of results (default 10)
    :returns: List of dicts with keys: title, url, points, author, comments

    Example::

        results = search_hackernews("genlayer", max_items=5)
    """
    url = f"https://hn.algolia.com/api/v1/search_by_date?query={query}&tags=story&hitsPerPage={max_items}"
    response = gl.get_from_web(url=url, mode="raw")
    data = json.loads(response)

    results = []
    for hit in data.get("hits", []):
        results.append({
            "title": hit.get("title", ""),
            "url": hit.get("url", ""),
            "points": hit.get("points", 0),
            "author": hit.get("author", ""),
            "comments": hit.get("num_comments", 0),
        })

    return results
