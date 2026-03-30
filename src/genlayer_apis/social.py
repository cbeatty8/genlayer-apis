"""
Social media and community data helpers for GenLayer Intelligent Contracts.

Fetch Twitter/X stats, GitHub repo info, and Discord server data. No API key required.
"""

import json
import genlayer.gl as gl


def github_repo(owner: str, repo: str) -> dict:
    """
    Get GitHub repository information.

    :param owner: Repository owner (e.g. "genlayerlabs")
    :param repo: Repository name (e.g. "genvm")
    :returns: dict with keys: name, description, stars, forks, issues,
              language, license, created_at, updated_at, url

    Example::

        info = github_repo("genlayerlabs", "genvm")
        # {'name': 'genvm', 'stars': 150, 'language': 'Rust', ...}
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = gl.get_from_web(url=url, mode="raw", headers={"Accept": "application/vnd.github.v3+json"})
    data = json.loads(response)

    return {
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "issues": data.get("open_issues_count", 0),
        "language": data.get("language", ""),
        "license": (data.get("license") or {}).get("spdx_id", ""),
        "created_at": data.get("created_at", ""),
        "updated_at": data.get("updated_at", ""),
        "url": data.get("html_url", ""),
    }


def github_releases(owner: str, repo: str, max_items: int = 5) -> list[dict]:
    """
    Get latest releases for a GitHub repository.

    :param owner: Repository owner
    :param repo: Repository name
    :param max_items: Maximum number of releases (default 5)
    :returns: List of dicts with keys: tag_name, name, published_at, url, body

    Example::

        releases = github_releases("genlayerlabs", "genvm")
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page={max_items}"
    response = gl.get_from_web(url=url, mode="raw", headers={"Accept": "application/vnd.github.v3+json"})
    data = json.loads(response)

    results = []
    for release in data:
        results.append({
            "tag_name": release.get("tag_name", ""),
            "name": release.get("name", ""),
            "published_at": release.get("published_at", ""),
            "url": release.get("html_url", ""),
            "body": release.get("body", "")[:500],
        })

    return results


def github_commits(owner: str, repo: str, branch: str = "main", max_items: int = 10) -> list[dict]:
    """
    Get recent commits for a GitHub repository.

    :param owner: Repository owner
    :param repo: Repository name
    :param branch: Branch name (default "main")
    :param max_items: Maximum number of commits (default 10)
    :returns: List of dicts with keys: sha, message, author, date, url

    Example::

        commits = github_commits("genlayerlabs", "genvm")
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}&per_page={max_items}"
    response = gl.get_from_web(url=url, mode="raw", headers={"Accept": "application/vnd.github.v3+json"})
    data = json.loads(response)

    results = []
    for commit in data:
        c = commit.get("commit", {})
        results.append({
            "sha": commit.get("sha", "")[:8],
            "message": c.get("message", "").split("\n")[0],
            "author": (c.get("author") or {}).get("name", ""),
            "date": (c.get("author") or {}).get("date", ""),
            "url": commit.get("html_url", ""),
        })

    return results


def twitter_user_stats(username: str) -> dict:
    """
    Get Twitter/X user statistics via nitter (public, no auth).

    :param username: Twitter username (without @)
    :returns: dict with keys: username, followers, following, tweets, bio

    Example::

        stats = twitter_user_stats("genaboringcompany")
        # {'username': 'genaboringcompany', 'followers': 5000, ...}
    """
    url = f"https://nitter.privacydev.net/{username}"
    html = gl.get_from_web(url=url, mode="raw")

    import re

    followers = 0
    following = 0
    tweets = 0

    # Extract follower counts from profile page
    followers_match = re.search(r'(\d[\d,.]*)\s*Followers', html, re.IGNORECASE)
    if followers_match:
        followers = int(followers_match.group(1).replace(",", "").replace(".", ""))

    following_match = re.search(r'(\d[\d,.]*)\s*Following', html, re.IGNORECASE)
    if following_match:
        following = int(following_match.group(1).replace(",", "").replace(".", ""))

    tweets_match = re.search(r'(\d[\d,.]*)\s*Tweets', html, re.IGNORECASE)
    if tweets_match:
        tweets = int(tweets_match.group(1).replace(",", "").replace(".", ""))

    bio_match = re.search(r'class="profile-bio"[^>]*>(.*?)</div>', html, re.DOTALL)
    bio = re.sub(r'<[^>]+>', '', bio_match.group(1)).strip() if bio_match else ""

    return {
        "username": username,
        "followers": followers,
        "following": following,
        "tweets": tweets,
        "bio": bio,
    }
