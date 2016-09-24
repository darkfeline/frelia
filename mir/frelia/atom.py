"""Atom feeds.

https://tools.ietf.org/html/rfc4287
"""

import abc
import xml.etree.ElementTree as ET

from mir.monads import maybe


def _make_subelement(element, tag, text):
    """Create subelement."""
    subelement = ET.SubElement(element, tag)
    subelement.text = text
    return subelement


def _make_subelement_if_not_none(element, tag, text):
    """Create a subelement if text is not None.

    Returns a Maybe monad.
    """
    if text is None:
        return maybe.Nothing()
    else:
        return maybe.Just(_make_subelement(element, tag, text))


def _extend_as_xml(element, constructs):
    """Extend element with constructs converted to XML elements."""
    element.extend(construct.to_xml() for construct in constructs)


class Feed:

    """Atom feed."""

    def __init__(
            self,
            id,
            title,
            updated,
            rights=None,
            links=(),
            authors=(),
            entries=()):
        self.id = id
        self.title = title
        self.updated = updated
        self.rights = rights
        self.links = links
        self.authors = authors
        self.entries = entries

    def to_xml(self):
        """Return ElementTree representation."""
        entry = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')
        _make_subelement(entry, 'id', self.id)
        _make_subelement(entry, 'title', self.title)
        _make_subelement(entry, 'updated', self.updated.isoformat())
        _make_subelement_if_not_none(entry, 'rights', self.rights)
        _extend_as_xml(entry, self.links)
        _extend_as_xml(entry, self.authors)
        _extend_as_xml(entry, self.entries)
        return entry

    def render(self, file):
        """Render Atom feed to a file.

        file should be in text mode.
        """
        element = self.to_xml()
        document = ET.ElementTree(element)
        document.write(file, encoding='unicode', xml_declaration=True)


class Entry:

    """Atom entry."""

    def __init__(
            self,
            id,
            title,
            updated,
            summary=None,
            published=None,
            links=(),
            categories=()):
        self.id = id
        self.title = title
        self.updated = updated
        self.summary = summary
        self.published = published
        self.links = links
        self.categories = categories

    def to_xml(self):
        """Return ElementTree representation."""
        entry = ET.Element('entry')
        _make_subelement(entry, 'id', self.id)
        _make_subelement(entry, 'title', self.title)
        _make_subelement(entry, 'updated', self.updated.isoformat())
        summary = _make_subelement_if_not_none(entry, 'summary', self.summary)
        summary.bind(_set_html_type)
        _make_subelement_if_not_none(entry, 'published',
                                     self.published.isoformat())
        _extend_as_xml(entry, self.links)
        _extend_as_xml(entry, self.categories)
        return entry


@maybe.monadic
def _set_html_type(element):
    """Set an Atom element to have HTML type content."""
    element.set('type', 'html')
    return element


class Person:

    """Atom person construct."""

    def __init__(self, name, uri=None, email=None):
        self.name = name
        self.uri = uri
        self.email = email

    @property
    @abc.abstractmethod
    def ELEMENT_TYPE(self):
        raise NotImplementedError

    def add_to(self, element):
        """Add person construct to element."""
        _make_subelement(element, 'name', self.name)
        _make_subelement_if_not_none(element, 'uri', self.uri)
        _make_subelement_if_not_none(element, 'email', self.email)


class Author:
    """Atom author metadata."""

    def __init__(self, name, uri=None, email=None):
        self.person = Person(name=name,
                             uri=uri,
                             email=email)

    def to_xml(self):
        """Return ElementTree representation."""
        entry = ET.Element('author')
        self.person.add_to(entry)
        return entry


def _set_attr_if_not_none(element, attr, value):
    """Set element attribute if value isn't None."""
    if value is not None:
        element.set(attr, value)


class Link:

    """Atom link metadata."""

    def __init__(self, href, rel=None, type=None):
        self.href = href
        self.rel = rel
        self.type = type

    def to_xml(self):
        """Return ElementTree representation."""
        element = ET.Element('link', href=self.href)
        _set_attr_if_not_none(element, 'rel', self.rel)
        _set_attr_if_not_none(element, 'type', self.type)
        return element


class Category:

    """Atom category metadata."""

    def __init__(self, term, scheme=None, label=None):
        self.term = term
        self.scheme = scheme
        self.label = label

    def to_xml(self):
        """Return ElementTree representation."""
        element = ET.Element('category', term=self.term)
        _set_attr_if_not_none(element, 'scheme', self.scheme)
        _set_attr_if_not_none(element, 'label', self.label)
        return element
