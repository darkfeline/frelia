"""Atom feed generator

This module contains classes representing RFC 4287 Atom documents and elements.
The classes have required and optional attributes corresponding to the elements
in the RFC.  Elements have a method, to_xml(), that returns an ElementTree
representation of themselves.  Documents can be rendered to files using
render().

Currently, not all Atom documents and elements are implemented.

Classes:

Feed -- Atom Feed Document
Entry

https://tools.ietf.org/html/rfc4287
"""

import datetime
import functools
import io
import typing
import xml.etree.ElementTree as ET

from mir.monads import maybe


class Document:

    """Atom Document.

    Documents are created with a root element and support rendering to a file.
    """

    def __init__(self, root_element: ET.Element):
        self.root = root_element

    def render(self, file: io.TextIOBase):
        """Render document to the file."""
        document = ET.ElementTree(self.root)
        document.write(file, encoding='unicode', xml_declaration=True)


def Feed(id, title, updated, rights=None, links=(), authors=(), entries=()):
    """Atom Feed element constructor."""
    element = ET.Element('feed')
    element.set('xmlns', 'http://www.w3.org/2005/Atom')
    _TextSubElement(element, ID, id)
    _TextSubElement(element, Title, title)
    _TextSubElement(element, Updated, updated)
    _MaybeTextSubElement(element, Rights, rights)
    element.extend(links)
    element.extend(authors)
    element.extend(entries)
    return element


def Entry(id, title, updated, summary=None, published=None, links=(),
          categories=()):
    """Atom Entry element constructor."""
    element = ET.Element('entry')
    _TextSubElement(element, ID, id)
    _TextSubElement(element, Title, title)
    _TextSubElement(element, Updated, updated)
    _MaybeTextSubElement(element, Summary, summary)
    _MaybeTextSubElement(element, Published, published)
    element.extend(links)
    element.extend(categories)
    return element


def _init_person(self, name, uri=None, email=None):
    """Atom Person construct constructor.

    This function is a detached method.
    """
    _TextSubElement(self, Name, name)
    _MaybeTextSubElement(self, URI, uri)
    _MaybeTextSubElement(self, Email, email)


def Author(name, uri=None, email=None):
    """Atom Author metadata element constructor."""
    element = ET.Element('author')
    _init_person(element, name, uri, email)
    return element


def Link(href, rel=None, type=None):
    """Atom Link metadata element constructor."""
    element = ET.Element('link')
    element.set('href', href)
    _maybe_set(element, 'rel', rel)
    _maybe_set(element, 'type', type)
    return element


def Category(term, scheme=None, label=None):
    """Atom Category metadata element constructor."""
    element = ET.Element('category')
    element.set('term', term)
    _maybe_set(element, 'scheme', scheme)
    _maybe_set(element, 'label', label)
    return element


def _maybe_set(self: ET.Element, key: str, value: typing.Optional[str]):
    """Set the attribute key to value if value isn't None.

    This function is a detached method.
    """
    if value is not None:
        self.set(key, value)


def _TextElement(tag: str, text_construct: 'TextConstruct'):
    """Text Element constructor.

    This represents an Atom Element that contains only a Text Construct.
    """
    element = ET.Element(tag)
    element.text = str(text_construct)
    text_construct.set_type(element)
    return element


class TextConstruct:

    """Text Construct.

    Represents an Atom Text Construct, which is basically a string with an
    optional type.
    """

    def __init__(self, text='', type=None):
        self._text = text
        self._type = type

    def __repr__(self):
        return '{cls}({object!r}, type={type!r})'.format(
            cls=type(self).__qualname__,
            object=self._text,
            type=self._type)

    def __str__(self):
        return self._text

    def set_type(self, element):
        """Set the type attribute of the element."""
        if self._type is not None:
            element.set('type', self._type)


ID = functools.partial(_TextElement, 'id')
Title = functools.partial(_TextElement, 'title')
Rights = functools.partial(_TextElement, 'rights')
Name = functools.partial(_TextElement, 'name')
Summary = functools.partial(_TextElement, 'summary')
URI = functools.partial(_TextElement, 'uri')
Email = functools.partial(_TextElement, 'email')


def _DataElement(tag: str, dt: datetime.date):
    """Construct an Atom Element that contains only a Date Construct."""
    assert isinstance(dt, datetime.date)
    return _TextElement(tag, (TextConstruct(dt.isoformat())))


Published = functools.partial(_DataElement, 'published')
Updated = functools.partial(_DataElement, 'updated')


def _TextSubElement(element: ET.Element, sub_type, text):
    """Create a subelement with given text value.

    If text is a string, it will be coerced into a TextConstruct.
    """
    if isinstance(text, str):
        text = TextConstruct(text)
    subelement = sub_type(text)
    element.append(subelement)
    return subelement


def _MaybeTextSubElement(element: ET.Element, sub_type, text):
    """Create a subelement with given text value if text is not None.

    Returns a Maybe monad.
    """
    if text is None:
        return maybe.Nothing()
    else:
        return maybe.Just(_TextSubElement(element, sub_type, text))
