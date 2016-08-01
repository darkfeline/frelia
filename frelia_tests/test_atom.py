import datetime

import pytest

from frelia import atom


@pytest.fixture
def feed():
    return atom.Feed(
        id='frelia',
        title='Frelia',
        updated=datetime.datetime(2010, 1, 2),
        authors=[atom.Author('darkfeline')],
        entries=[
            atom.Entry(
                id='post',
                title='Post',
                updated=datetime.datetime(2010, 3, 4),
                links=[atom.Link('http://localhost/post')],
                categories=[atom.Category('news')])
        ])


def test_render(feed):
    got = atom.render(feed)
    assert got == """\
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

  <id>frelia</id>
  <title>Frelia</title>
  <updated>2010-01-02T00:00:00</updated>

  <author>
    <name>darkfeline</name>
  </author>

  <entry>
    <id>post</id>
    <title>Post</title>
    <updated>2010-03-04T00:00:00</updated>
    <link href="http://localhost/post" />
    <category term="news" />
  </entry>
</feed>"""
