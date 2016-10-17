"""Atom feed generator

Classes:

Feed -- Atom feed root element
Entry -- Feed entry element

Author -- Author metadata element
Link -- Link metadata element
Category -- Category metadata element

https://tools.ietf.org/html/rfc4287
"""

import datetime
import functools
import io
import itertools
import xml.etree.ElementTree as ET


class Feed:

    def __init__(self, id, title, updated: datetime.date):
        self.id = id
        self.title = title
        self.updated = updated
        self.rights = ''
        self.categories = []
        self.entries = []

    def _to_etree(self):
        element = ET.Element('feed')
        element.set('xmlns', 'http://www.w3.org/2005/Atom')
        element.append(_ID(self.id))
        element.append(_Title(self.title))
        element.append(_Updated(self.updated))
        element.extend(
            item._to_xml()
            for item in itertools.chain(self.categories, self.entries)
        )
        return element

    def write(self, file: io.TextIOBase):
        """Write XML document to file."""
        document = ET.ElementTree(self._to_etree())
        document.write(file, encoding='unicode', xml_declaration=True)


class Entry:

    def __init__(self, id, title, updated: datetime.date):
        self.id = id
        self.title = title
        self.updated = updated
        self.published = None
        self.summary = ''
        self.links = []
        self.authors = []
        self.categories = []
        self.entries = []

    def _to_etree(self):
        element = ET.Element('entry')
        element.set('xmlns', 'http://www.w3.org/2005/Atom')
        element.append(_ID(self.id))
        element.append(_Title(self.title))
        element.append(_Updated(self.updated))
        if self.published:
            element.append(_Published(self.published))
        if self.summary:
            element.append(_Summary(self.summary))
        element.extend(
            item._to_xml()
            for item in itertools.chain(
                self.links, self.authors, self.categories, self.entries)
        )
        return element


class _Person:

    def __init__(self, name):
        self.name = name
        self.uri = ''
        self.email = ''

    def _to_etree(self):
        element = ET.Element(self._TAG)
        element.append(_Name(self.name))
        if self.uri:
            element.append(_URI(self.uri))
        if self.email:
            element.append(_Email(self.email))
        return element


class Author(_Person):
    _TAG = 'author'


class Link:

    def __init__(self, href):
        self.href = href
        self.rel = ''
        self.type = ''

    def _to_etree(self):
        element = ET.Element('link')
        element.set('href', self.href)
        if self.rel:
            element.set('rel', self.rel)
        if self.type:
            element.set('type', self.type)
        return element


class Category:

    def __init__(self, term):
        self.term = term
        self.scheme = ''
        self.label = ''

    def _to_etree(self):
        element = ET.Element('category')
        element.set('term', self.term)
        if self.scheme:
            element.set('scheme', self.scheme)
        if self.label:
            element.set('label', self.label)
        return element


def _TextElement(tag, text, type=''):
    element = ET.Element(tag)
    element.text = text
    if type:
        element.set('type', type)
    return element


def _DateElement(tag, date: datetime.date):
    element = ET.Element(tag)
    element.text = date.isoformat()
    return element


_ID = functools.partial(_TextElement, 'id')
_Title = functools.partial(_TextElement, 'title')
_Rights = functools.partial(_TextElement, 'rights')
_Name = functools.partial(_TextElement, 'name')
_Summary = functools.partial(_TextElement, 'summary')
_URI = functools.partial(_TextElement, 'uri')
_Email = functools.partial(_TextElement, 'email')

_Published = functools.partial(_DateElement, 'published')
_Updated = functools.partial(_DateElement, 'updated')
