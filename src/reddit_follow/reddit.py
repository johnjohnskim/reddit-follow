"""Reddit

Access the Reddit API to fetch posts from the target subreddit(s).
"""

import requests

from .last_runtime import LastRuntimeHandler

USER_AGENT = "Follow Script JK"


class RedditError(Exception):
    pass


def create_access_token(client_id, client_secret, reddit_username, reddit_password):
    """Create a new Reddit access token (of type 'password')."""
    url = "https://www.reddit.com/api/v1/access_token"
    data = {
        "grant_type": "password",
        "username": reddit_username,
        "password": reddit_password,
    }
    headers = {
        "User-Agent": USER_AGENT,
    }

    resp = requests.post(url, data, headers=headers, auth=(client_id, client_secret))
    if resp.status_code != 200:
        raise RedditError(f"Bad response code: {resp.status_code}", resp.content)
    return resp.json()["access_token"]


def get_posts(token, subreddit, query, limit=25, t="hour", after=None):
    """Fetch recent posts in the target subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {
        "q": query,
        "restrict_sr": "on",
        "sort": "new",
        "limit": limit,
        "t": t,
        "after": after,
    }
    headers = {
        "Authorization": token,
        "User-Agent": USER_AGENT,
    }

    resp = requests.get(url, params, headers=headers)
    if resp.status_code != 200:
        raise RedditError(f"Bad response code: {resp.status_code}", resp.content)
    return resp.json()["data"]


def get_all_posts(token, subreddit, query, last_runtime_handler=LastRuntimeHandler()):
    """Fetch all recent posts in the target subreddit."""
    data = get_posts(token, subreddit, query)
    posts = data["children"]

    if not posts:
        return []

    while data.get("after"):
        data = get_posts(token, subreddit, query, after=data["after"])
        posts.extend(data["children"])

    def get_created_time(post):
        return post["data"]["created_utc"]

    posts = sorted(posts, key=get_created_time)
    most_recently_created = get_created_time(posts[-1])
    last_runtime = last_runtime_handler.get_last_runtime(subreddit)
    if last_runtime:
        # Ignore posts we've already seen.
        posts = [p for p in posts if get_created_time(p) > last_runtime]
    last_runtime_handler.set_last_runtime(subreddit, most_recently_created)

    return posts
