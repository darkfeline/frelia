import collections
import datetime
import io

import pytest

from mir.frelia import atom


@pytest.mark.parametrize(
    ('id', 'title', 'updated'),
    [('http://example.com/', 'Takumi Times', datetime.datetime(2016, 1, 8))]
)
def test_render(id, title, updated):
    """Test document rendering."""
    feed = atom.Feed(id, title, updated)
    document = atom.Document(feed)
    file = io.StringIO()
    document.render(file)
    assert file.getvalue() == (
        "<?xml version='1.0' encoding='UTF-8'?>\n"
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        '<id>http://example.com/</id>'
        '<title>Takumi Times</title><updated>2016-01-08T00:00:00</updated>'
        '</feed>')


_FEED_PARAMS = ('id', 'title', 'updated', 'rights', 'links', 'authors',
                'entries')
_FeedTest = collections.namedtuple('_FeedTest', _FEED_PARAMS)


@pytest.mark.parametrize(
    _FEED_PARAMS,
    [_FeedTest(
        id='http://example.com/',
        title='Takumi Times',
        updated=datetime.datetime(2016, 1, 8),
        rights='Public Domain',
        links=(),
        authors=(),
        entries=())])
def test_feed(id, title, updated, rights, links, authors, entries):
    """Test Feed.to_xml()."""
    element = atom.Feed(id, title, updated, rights, links, authors, entries)
    assert element.tag == 'feed'
    assert element.find('id').text == id
    assert element.find('title').text == title
    assert element.find('updated').text == updated.isoformat()
    assert element.find('rights').text == rights


_ENTRY_PARAMS = ('id', 'title', 'updated', 'summary', 'summary_type',
                 'published', 'links', 'categories')
_EntryTest = collections.namedtuple('_EntryTest', _ENTRY_PARAMS)


@pytest.mark.parametrize(
    _ENTRY_PARAMS,
    [_EntryTest(
        id='http://example.com/pandora',
        title='Pandora',
        updated=datetime.datetime(2016, 1, 8),
        summary='Girl meets girl',
        summary_type='html',
        published=datetime.datetime(2012, 10, 10),
        links=(),
        categories=())])
def test_entry(id, title, updated, summary, summary_type, published, links,
               categories):
    """Test Entry.to_xml()."""
    element = atom.Entry(
        id=id,
        title=title,
        updated=updated,
        summary=atom.TextConstruct(summary, type=summary_type),
        published=published,
        links=links,
        categories=categories)
    assert element.tag == 'entry'
    assert element.find('id').text == id
    assert element.find('title').text == title
    assert element.find('updated').text == updated.isoformat()
    assert element.find('summary').text == summary
    assert element.find('summary').get('type') == summary_type
    assert element.find('published').text == published.isoformat()


@pytest.mark.parametrize(
    ('name', 'uri', 'email'),
    [('Nene', 'http://example.com/', 'dork@example.com')])
def test_author(name, uri, email):
    """Test Author.to_xml()."""
    element = atom.Author(name, uri, email)
    assert element.tag == 'author'
    assert element.find('name').text == name
    assert element.find('uri').text == uri
    assert element.find('email').text == email


@pytest.mark.parametrize('term,scheme,label', [
    ('dork', 'http://example.com/', 'Nene'),
    ('dork', 'http://example.com/', None),
])
def test_category(term, scheme, label):
    """Test Category.to_xml()."""
    element = atom.Category(term, scheme, label)
    assert element.tag == 'category'
    assert element.get('term', None) == term
    assert element.get('scheme', None) == scheme
    assert element.get('label', None) == label


@pytest.mark.parametrize(
    ('href', 'rel', 'type'),
    [('http://example.com/', 'alternate', 'text/html')])
def test_link(href, rel, type):
    """Test Link."""
    element = atom.Link(href, rel, type)
    assert element.tag == 'link'
    assert element.get('href', None) == href
    assert element.get('rel', None) == rel
    assert element.get('type', None) == type
