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


def test_feed():
    """Test Feed."""
    element = atom.Feed(
        id='http://example.com/',
        title='Example site',
        updated=datetime.datetime(2016, 1, 8))

    assert element.tag == 'feed'
    assert element.find('id').text == 'http://example.com/'
    assert element.find('title').text == 'Example site'
    assert element.find('updated').text == '2016-01-08T00:00:00'


def test_entry():
    """Test Entry."""
    element = atom.Entry(
        id='http://example.com/pandora',
        title='Pandora',
        updated=datetime.datetime(2016, 1, 8))
    assert element.tag == 'entry'
    assert element.find('id').text == 'http://example.com/pandora'
    assert element.find('title').text == 'Pandora'
    assert element.find('updated').text == '2016-01-08T00:00:00'


def test_author():
    """Test Author."""
    element = atom.Author('Nene')
    element.append(atom.URI('http://example.com/'))
    element.append(atom.Email('dork@example.com'))
    assert element.tag == 'author'
    assert element.find('name').text == 'Nene'
    assert element.find('uri').text == 'http://example.com/'
    assert element.find('email').text == 'dork@example.com'


def test_category():
    """Test Category."""
    element = atom.Category('dork')
    element.set_scheme('http://example.com/')
    element.set_label('Nene')
    assert element.tag == 'category'
    assert element.get('term', None) == 'dork'
    assert element.get('scheme', None) == 'http://example.com/'
    assert element.get('label', None) == 'Nene'


def test_link():
    """Test Link."""
    element = atom.Link('http://example.com/')
    element.set_rel('alternate')
    element.set_type('text/html')
    assert element.tag == 'link'
    assert element.get('href', None) == 'http://example.com/'
    assert element.get('rel', None) == 'alternate'
    assert element.get('type', None) == 'text/html'


def test__elem_identity():
    """Test _elem returns Element."""
    element = ET.Element('h1')
    assert atom._elem(element) is element


def test__elem_type_error():
    """Test _elem on bad type."""
    with pytest.raises(TypeError):
        atom._elem(object())


def test__Element_text():
    """Test _Element text property."""
    element = atom._Element('h1')
    element.text = 'test'
    assert element.text == 'test'


def test__Element_extend():
    """Test _Element extend()."""
    element = atom._Element('h1')
    children = [ET.Element('p')]
    element.extend(children)
    assert list(element) == children


def test__TextElement_TextConstruct():
    """Test _TextElement with TextConstruct."""
    element = atom._TextElement(
        tag='title',
        text=atom.TextConstruct('hello', type='html'))
    assert element.get('type', 'html')
    assert element.text == 'hello'
