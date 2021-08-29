from reddit_follow.match import has_digits, has_matching_post, parse_title_search


def test_parse_title_search_one_phrase():
    expected = {"allowlist": ["foo bar"], "blocklist": []}
    assert parse_title_search("foo bar") == expected


def test_parse_title_search_multi_words():
    expected = {"allowlist": ["foo bar", "baz"], "blocklist": []}
    assert parse_title_search("foo bar,baz") == expected


def test_parse_title_search_filter_words():
    expected = {"allowlist": ["foo bar", "baz"], "blocklist": ["boop", "beep"]}
    assert parse_title_search("foo bar,baz--boop,beep") == expected


def test_match_post_one_phrase():
    target_titles = [
        {"allowlist": ["foo bar"], "blocklist": []},
        {"allowlist": ["fool"], "blocklist": []},
    ]
    title = "[DISC] Foo bar here"  # case-insensitive
    assert has_matching_post(title, target_titles)

    title = "[DISC} Bar foo here"
    assert not has_matching_post(title, target_titles)


def test_match_post_multi_words():
    target_titles = [{"allowlist": ["foo", "bar"], "blocklist": []}]
    title = "[DISC] foo gibberish bar"
    assert has_matching_post(title, target_titles)

    title = "[DISC] foo gibberish here"
    assert not has_matching_post(title, target_titles)


def test_match_post_filter_words():
    target_titles = [{"allowlist": ["foo", "bar"], "blocklist": ["baz", "bing"]}]
    title = "[DISC] foo gibberish bar boop baz"
    assert not has_matching_post(title, target_titles)

    title = "[DISC] foo bing bar boop"
    assert not has_matching_post(title, target_titles)

    title = "[DISC] foo gibberish bar"
    assert has_matching_post(title, target_titles)


def test_has_digits():
    assert has_digits("foo bar ch. 123")
    assert has_digits("foo bar 123 (bee)")
    assert not has_digits("foo bar ch.")
