import datetime
import io
import xml.etree.ElementTree as ET

import pytest

from mir.frelia import atom


def test_render():
    """Test document rendering."""
    feed = atom.Feed(
        id='http://example.com/',
        title='Example site',
        updated=datetime.datetime(2016, 1, 8))
    file = io.StringIO()
    feed.write(file)
    assert file.getvalue() == (
        "<?xml version='1.0' encoding='UTF-8'?>\n"
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        '<id>http://example.com/</id>'
        '<title>Example site</title><updated>2016-01-08T00:00:00</updated>'
        '</feed>')


def test_feed_to_etree():
    """Test Feed."""
    feed = atom.Feed(
        id='http://example.com/',
        title='Example site',
        updated=datetime.datetime(2016, 1, 8))
    feed.entries.append(atom.Entry(
        id='http://example.com/pandora',
        title='Pandora',
        updated=datetime.datetime(2016, 1, 8)))

    element = feed.to_etree()
    assert element.tag == 'feed'
    assert element.find('id').text == 'http://example.com/'
    assert element.find('title').text == 'Example site'
    assert element.find('updated').text == '2016-01-08T00:00:00'
    assert element.find('entry').find('id').text == 'http://example.com/pandora'


def test_entry_to_etree():
    """Test Entry.to_etree()."""
    entry = atom.Entry(
        id='http://example.com/pandora',
        title='Pandora',
        updated=datetime.datetime(2016, 1, 8))
    element = entry.to_etree()
    assert element.tag == 'entry'
    assert element.find('id').text == 'http://example.com/pandora'
    assert element.find('title').text == 'Pandora'
    assert element.find('updated').text == '2016-01-08T00:00:00'


def test_full_entry_to_etree():
    """Test full Entry.to_etree()."""
    entry = atom.Entry(
        id='http://example.com/pandora',
        title='Pandora',
        updated=datetime.datetime(2016, 1, 8))
    entry.published = datetime.datetime(2016, 1, 9)
    entry.summary = 'girl meets girl'
    entry.authors.append(atom.Author('Nene'))
    element = entry.to_etree()
    assert element.tag == 'entry'
    assert element.find('id').text == 'http://example.com/pandora'
    assert element.find('title').text == 'Pandora'
    assert element.find('updated').text == '2016-01-08T00:00:00'
    assert element.find('published').text == '2016-01-09T00:00:00'
    assert element.find('summary').text == 'girl meets girl'
    assert element.find('author').find('name').text == 'Nene'


def test_author_to_etree():
    """Test Author.to_etree()."""
    author = atom.Author('Nene')
    element = author.to_etree()
    assert element.tag == 'author'
    assert element.find('name').text == 'Nene'
    assert element.find('uri') is None
    assert element.find('email') is None


def test_full_author_to_etree():
    """Test full Author.to_etree()."""
    author = atom.Author('Nene')
    author.uri = 'http://example.com/'
    author.email = 'dork@example.com'
    element = author.to_etree()
    assert element.tag == 'author'
    assert element.find('name').text == 'Nene'
    assert element.find('uri').text == 'http://example.com/'
    assert element.find('email').text == 'dork@example.com'


def test_link_to_etree():
    """Test Link.to_etree()."""
    link = atom.Link('http://example.com/')
    element = link.to_etree()
    assert element.tag == 'link'
    assert element.get('href', None) == 'http://example.com/'
    assert element.get('rel', None) is None
    assert element.get('type', None) is None


def test_full_link_to_etree():
    """Test full Link.to_etree()."""
    link = atom.Link('http://example.com/')
    link.rel = 'alternate'
    link.type = 'text/html'
    element = link.to_etree()
    assert element.tag == 'link'
    assert element.get('href', None) == 'http://example.com/'
    assert element.get('rel', None) == 'alternate'
    assert element.get('type', None) == 'text/html'


def test_category_to_etree():
    """Test Category.to_etree()."""
    category = atom.Category('dork')
    element = category.to_etree()
    assert element.tag == 'category'
    assert element.get('term', None) == 'dork'
    assert element.get('scheme', None) is None
    assert element.get('label', None) is None


def test_full_category_to_etree():
    """Test full Category.to_etree()."""
    category = atom.Category('dork')
    category.scheme = 'http://example.com/'
    category.label = 'Nene'
    element = category.to_etree()
    assert element.tag == 'category'
    assert element.get('term', None) == 'dork'
    assert element.get('scheme', None) == 'http://example.com/'
    assert element.get('label', None) == 'Nene'


def test__TextElement_type():
    """Test _TextElement with type."""
    element = atom._TextElement(
        tag='summary',
        text='girl meets girl',
        type='text/html')
    assert element.get('type') == 'text/html'
