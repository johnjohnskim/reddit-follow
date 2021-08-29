"""Slack

Notification functions to send Slack messages to a designated webhook URL.
"""

import re

import requests


class SlackError(Exception):
    pass


def clean_link(link):
    """Replace imgur album links with their guya.moe equivalent."""
    # Remove the "m." in mobile links
    link = re.sub(r"\bm\.", "", link)
    return re.sub(r"imgur\.com\/a\/", "cubari.moe/read/imgur/", link)


def slack_message(webhook_url, message):
    """Send a message to the designated Slack Webhook URL."""
    resp = requests.post(webhook_url, json={"text": message})
    if resp.status_code != 200:
        raise SlackError("Could not send slack message", resp.content)
    return resp


def notify(webhook_url, subreddit, posts):
    """Send notifications for new posts via Slack."""
    messages = []

    for post in posts:
        data = post["data"]
        message = f"""\
<https://www.reddit.com/r/{subreddit}|/r/{subreddit}>: {data['title']}
Link: {clean_link(data['url'])}
Comments: https://www.reddit.com{data['permalink']}"""
        slack_message(webhook_url, message)
        messages.append(message)

    return messages
