"""Atom feeds.

https://tools.ietf.org/html/rfc4287

"""

import xml.etree.ElementTree as ET


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
        ET.SubElement(entry, 'id').text = self.id
        ET.SubElement(entry, 'title').text = self.title
        ET.SubElement(entry, 'updated').text = self.updated.isoformat()
        if self.rights is not None:
            ET.SubElement(entry, 'rights').text = self.rights
        entry.extend(link.to_xml() for link in self.links)
        entry.extend(author.to_xml() for author in self.authors)
        entry.extend(entry.to_xml() for entry in self.entries)
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
        ET.SubElement(entry, 'id').text = self.id
        ET.SubElement(entry, 'title').text = self.title
        ET.SubElement(entry, 'updated').text = self.updated.isoformat()
        if self.summary is not None:
            ET.SubElement(entry, 'summary', type='html').text = self.summary
        if self.published is not None:
            ET.SubElement(entry, 'published').text = self.published.isoformat()
        entry.extend(link.to_xml() for link in self.links)
        entry.extend(category.to_xml() for category in self.categories)
        return entry


class Person:

    """Atom person construct.

    Concrete subclasses must set the ELEMENT_TYPE class attribute.

    """

    def __init__(self, name, uri=None, email=None):
        self.name = name
        self.uri = uri
        self.email = email

    def to_xml(self):
        """Return ElementTree representation."""
        entry = ET.Element('author')
        ET.SubElement(entry, 'name').text = self.name
        if self.uri is not None:
            ET.SubElement(entry, 'uri').text = self.uri
        if self.email is not None:
            ET.SubElement(entry, 'email').text = self.email
        return entry


class Author(Person):

    """Atom author metadata."""

    ELEMENT_TYPE = 'author'


class Link:

    """Atom link metadata."""

    def __init__(self, href, rel=None, type=None):
        self.href = href
        self.rel = rel
        self.type = type

    def to_xml(self):
        """Return ElementTree representation."""
        element = ET.Element('link', href=self.href)
        if self.rel is not None:
            element.set('rel', self.rel)
        if self.type is not None:
            element.set('type', self.type)
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
        if self.scheme is not None:
            element.set('scheme', self.scheme)
        if self.label is not None:
            element.set('label', self.label)
        return element
