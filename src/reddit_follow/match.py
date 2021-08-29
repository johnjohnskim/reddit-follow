"""Match

Functions to match Reddit post titles against designated search terms.
"""

import re


def parse_title_search(search):
    """Parse a short-hand search into a more usable form."""
    parts = search.strip().split("--")
    parts = [p.split(",") for p in parts]
    return {
        "allowlist": parts[0],
        "blocklist": parts[1] if len(parts) > 1 else [],
    }


def has_matching_post(title, target_titles):
    """Check if the post title matches any of the target titles."""

    def has_allowlisted_terms(terms):
        return all(term.lower() in title for term in terms)

    def has_no_blocklisted_terms(terms):
        return all(term.lower() not in title for term in terms)

    title = title.lower()
    for t in target_titles:
        if has_allowlisted_terms(t["allowlist"]) and has_no_blocklisted_terms(t["blocklist"]):
            return True
    return False


def has_digits(title):
    """Check if the post title has a chapter or episode number."""
    return bool(re.search(r"\d+", title))


def find_matching_posts(posts, titles):
    """Filter out posts that don't match our approved title list."""
    return [
        post
        for post in posts
        if has_matching_post(post["data"]["title"], titles) and has_digits(post["data"]["title"])
    ]
