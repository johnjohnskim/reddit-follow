"""CLI

Command-line interface / main.
"""

import logging
import os
import os.path
from configparser import ConfigParser

import click

from . import __version__
from .last_runtime import LastRuntimeHandler
from .match import find_matching_posts, parse_title_search
from .reddit import create_access_token, get_all_posts
from .slack import notify

log = logging.getLogger(__name__)


def setup_logging():
    """Setup logging to print to stdout."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )


def get_file_path(filename):
    """Gets the full filepath for files in the top-level directory."""
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
    except NameError:
        log.info("running in local shell")
        dir_path = "."

    return os.path.join(dir_path, os.pardir, os.pardir, filename)


def load_settings():
    """Parse the various settings in settings.ini"""
    parser = ConfigParser()
    parser.read([os.getenv("SETTINGS_PATH") or get_file_path("settings.ini")])

    return {
        "client_id": parser["oauth"]["id"],
        "client_secret": parser["oauth"]["secret"],
        "reddit_username": parser["reddit"]["username"],
        "reddit_password": parser["reddit"]["password"],
        "slack_webhook_url": parser["slack"]["webhook_url"],
    }


def get_post_search_terms():
    """Get the list of post search terms from posts.ini"""
    parser = ConfigParser()
    parser.read([os.getenv("POSTS_PATH") or get_file_path("posts.ini")])

    searches = []
    for section in parser.sections():
        searches.append(
            (
                section,
                parser[section]["query"],
                [line.strip() for line in parser[section]["titles"].strip().splitlines()],
            )
        )
    return searches


@click.command()
@click.version_option(version=__version__)
def main():
    setup_logging()
    log.info("starting script")

    settings = load_settings()

    log.info("getting access token")
    token = create_access_token(
        settings["client_id"],
        settings["client_secret"],
        settings["reddit_username"],
        settings["reddit_password"],
    )

    last_runtime_handler = LastRuntimeHandler(host=os.getenv("REDIS_HOST") or "redis")
    post_search_terms = get_post_search_terms()

    for subreddit, query, search_terms in post_search_terms:
        log.info(f"fetching posts for /r/{subreddit}")
        posts = get_all_posts(token, subreddit, query, last_runtime_handler=last_runtime_handler)
        titles = [parse_title_search(search) for search in search_terms]
        matching_posts = find_matching_posts(posts, titles)

        if matching_posts:
            log.info(f"found {len(matching_posts)} relevant posts")
            messages = notify(settings["slack_webhook_url"], subreddit, matching_posts)
            for message in messages:
                log.info(message)
        else:
            log.info("no relevant posts found")

    log.info("ending script")


if __name__ == "__main__":
    main()
