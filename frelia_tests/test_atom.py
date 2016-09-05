import collections
import datetime
import io

import pytest

from frelia import atom


@pytest.mark.parametrize(
    ('id', 'title', 'updated'),
    [('http://example.com/', 'Takumi Times', datetime.datetime(2016, 1, 8))])
def test_render(id, title, updated):
    """Test Feed.render()."""
    feed = atom.Feed(id, title, updated)
    file = io.StringIO()
    feed.render(file)
    assert file.getvalue() == '''\
<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom"><id>http://example.com/</id>\
<title>Takumi Times</title><updated>2016-01-08T00:00:00</updated></feed>'''


_FEED_PARAMS = ('id', 'title', 'updated', 'rights', 'links', 'authors',
                'entries')
_FeedArgs = collections.namedtuple('_FeedArgs', _FEED_PARAMS)


@pytest.mark.parametrize(
    _FEED_PARAMS,
    [_FeedArgs(
        id='http://example.com/',
        title='Takumi Times',
        updated=datetime.datetime(2016, 1, 8),
        rights='Public Domain',
        links=(),
        authors=(),
        entries=())])
def test_feed(id, title, updated, rights, links, authors, entries):
    """Test Feed.to_xml()."""
    feed = atom.Feed(id, title, updated, rights, links, authors, entries)
    element = feed.to_xml()
    assert element.tag == 'feed'
    assert element.find('id').text == id
    assert element.find('title').text == title
    assert element.find('updated').text == updated.isoformat()
    assert element.find('rights').text == rights


_ENTRY_PARAMS = ('id', 'title', 'updated', 'summary', 'published', 'links',
                 'categories')
_EntryArgs = collections.namedtuple('_EntryArgs', _ENTRY_PARAMS)


@pytest.mark.parametrize(
    _ENTRY_PARAMS,
    [_EntryArgs(
        id='http://example.com/dork-meets-robot',
        title='Dork meets robot',
        updated=datetime.datetime(2016, 1, 8),
        summary='Girl meets girl daya',
        published=datetime.datetime(2012, 10, 10),
        links=(),
        categories=())])
def test_entry(id, title, updated, summary, published, links, categories):
    """Test Entry.to_xml()."""
    entry = atom.Entry(id, title, updated, summary, published, links,
                       categories)
    element = entry.to_xml()
    assert element.tag == 'entry'
    assert element.find('id').text == id
    assert element.find('title').text == title
    assert element.find('updated').text == updated.isoformat()
    assert element.find('summary').text == summary
    assert element.find('published').text == published.isoformat()


@pytest.mark.parametrize(
    ('name', 'uri', 'email'),
    [('Nene', 'http://example.com/', 'dork@example.com')])
def test_author(name, uri, email):
    """Test Author.to_xml()."""
    author = atom.Author(name, uri, email)
    element = author.to_xml()
    assert element.tag == 'author'
    assert element.find('name').text == name
    assert element.find('uri').text == uri
    assert element.find('email').text == email


@pytest.mark.parametrize(
    ('term', 'scheme', 'label'),
    [('dork', 'http://example.com/', 'Nene')])
def test_category(term, scheme, label):
    """Test Category.to_xml()."""
    category = atom.Category(term, scheme, label)
    element = category.to_xml()
    assert element.tag == 'category'
    assert element.attrib == {
        'term': term,
        'scheme': scheme,
        'label': label,
    }


@pytest.mark.parametrize(
    ('href', 'rel', 'type'),
    [('http://example.com/', 'alternate', 'text/html')])
def test_link(href, rel, type):
    """Test Link.to_xml()."""
    link = atom.Link(href, rel, type)
    element = link.to_xml()
    assert element.tag == 'link'
    assert element.attrib == {
        'href': href,
        'rel': rel,
        'type': type,
    }
