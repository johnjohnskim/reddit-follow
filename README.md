# reddit-follow

Notifies you via Slack about posts that may appear in a specific subreddit. I use this to follow
new chapter or episode releases for ongoing series. This relies on the Reddit
[/r/manga](https://www.reddit.com/r/manga/) subreddit's users to post new discussion threads
everytime a new chapter is released. For the mangas and shows I follow, this is quite reliable!

The script will send you messages formatted like:

> Title: [DISC] Shingeki no Kyojin - Chapter 130 \
> Link: https://example.com/gallery/abcdefg \
> Comments: https://www.reddit.com/r/manga/comments/hmj78x/disc_shingeki_no_kyojin_chapter_130/

## Post Titles

To list the posts you want to be notified about, update the file `posts.ini` located in this
directory.

- The `section` name should contain the name of the target subreddit, e.g. `manga` for /r/manga.
- The `query` variable should contain any tags or words that will match all relevant post titles,
  e.g. `title:[DISC]` will look for all post titles containing "[DISC]".
- The `titles` variable should contain a newline-separated list of all desired post titles.
  - To look for an exact match, simply list the full title, e.g. `One Piece`.
  - If the title may be variable, you can list comma-separated keywords to search for, e.g.
    `One,Piece`.
  - If there are keywords you want to avoid matching on, use `--`. For example, `One Piece--fan`
    will match on "One Piece", but avoid any thread titles that also contain the word "fan".

```ini
[manga]
; All chapter release posts should be tagged as "discussion" ([DISC]) posts.
query = title:[DISC]
titles =
  shingeki no kyojin
  attack on titan

[anime]
; All episode discussion posts should have an "episode" flair.
query = flair:episode
titles =
  shingeki no kyojin
  attack on titan
```

## To run

You will need [Reddit API access](https://www.reddit.com/wiki/api), a Reddit account, and a valid
[Slack Webhook URL](https://api.slack.com/messaging/webhooks). Once you've obtained the
necessary accounts and access, create a file named `settings.ini` in this directory, with the
following:

```ini
[oauth]
; Your Reddit OAUTH client ID and secret.
id = abcdef
secret = ghi-jklm

[reddit]
; Your Reddit account's username and password.
username = someusername
password = somepassword

[slack]
; Your Slack Webhook URL.
webhook_url = https://hooks.slack.com/services/FAKE/URL/here
```

### With Docker + Docker-compose

Run:

#### `make build && make run`

This will also create a separate container for the Redis server.

### Without Docker

This assumes you have the necessary python3 instance, [Poetry](https://python-poetry.org/), and any
required packages installed. By default, you will also need a running Redis server.

Run:

#### `poetry run reddit-follow`

You may also want to use the following environment variables:

- `SETTINGS_PATH`: the full filepath to the `settings.ini` file.
- `POSTS_PATH`: the full filepath to the `posts.ini` file.
- `REDIS_HOST`: the host of the Redis server.
