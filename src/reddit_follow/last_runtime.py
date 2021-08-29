"""Last Runtime

Handler for the last time posts were fetched.
"""

import time

import redis


class LastRuntimeHandler:
    """Handler for the last time posts were fetched."""

    def __init__(self, host="localhost"):
        self.r = redis.Redis(host=host)
        self.base_key = "last_runtime"

    def get_key(self, subreddit):
        return f"{self.base_key}:{subreddit}"

    def get_last_runtime(self, subreddit):
        last_runtime = self.r.get(self.get_key(subreddit))
        return float(last_runtime) if last_runtime else None

    def set_last_runtime(self, subreddit, last_runtime=None):
        return self.r.set(self.get_key(subreddit), last_runtime or time.time())
