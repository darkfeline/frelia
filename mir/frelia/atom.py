"""Atom feed generator

Classes:

Feed -- Atom feed root element
Entry -- Feed entry element

Author -- Author metadata element
Link -- Link metadata element
Category -- Category metadata element

ID -- ID metadata element
Title -- Title metadata element
Rights -- Rights metadata element
Name -- Name metadata element
Summary -- Summary metadata element
URI -- URI metadata element
Email -- Email metadata element

Published -- Published metadata element
Updated -- Updated metadata element

TextConstruct -- Atom text construct

https://tools.ietf.org/html/rfc4287
"""

import collections
import datetime
import functools
import io
import xml.etree.ElementTree as ET


def _elem(object):
    """Type casting for Element.

    This is needed because subclassing etree classes breaks them, so we must
    encapsulate them and pretend we're subclassing.
    """
    if isinstance(object, ET.Element):
        return object
    elif isinstance(object, _Element):
        return object._element
    else:
        raise TypeError('Invalid element %r' % object)


class _Element:

    """Pretend subclass of etree.Element."""

    def __init__(self, *args, **kwargs):
        self._element = ET.Element(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._element, name)

    def __iter__(self):
        return iter(self._element)

    @property
    def text(self):
        return self._element.text

    @text.setter
    def text(self, value):
        self._element.text = value

    def append(self, element):
        """Add entry or metadata element."""
        self._element.append(_elem(element))

    def extend(self, elements):
        self._element.extend(_elem(element) for element in elements)


class Feed(_Element):

    def __init__(self, id, title, updated: datetime.date):
        super().__init__('feed')
        self.set('xmlns', 'http://www.w3.org/2005/Atom')
        self.append(ID(id))
        self.append(Title(title))
        self.append(Updated(updated))

    def write(self, file: io.TextIOBase):
        """Write XML document to file."""
        document = ET.ElementTree(self._element)
        document.write(file, encoding='unicode', xml_declaration=True)


class Entry(_Element):

    def __init__(self, id, title, updated: datetime.date):
        super().__init__('entry')
        self.append(ID(id))
        self.append(Title(title))
        self.append(Updated(updated))


class _Person(_Element):

    def __init__(self, tag, name):
        super().__init__(tag)
        self.append(Name(name))


class Author(_Person):

    def __init__(self, name):
        super().__init__(tag='author', name=name)


class Link(_Element):

    def __init__(self, href):
        super().__init__('link')
        self.set('href', href)

    def set_rel(self, rel):
        self.set('rel', rel)

    def set_type(self, type):
        self.set('type', type)


class Category(_Element):

    def __init__(self, term):
        super().__init__('category')
        self.set('term', term)

    def set_scheme(self, scheme):
        self.set('scheme', scheme)

    def set_label(self, label):
        self.set('label', label)


class _TextElement(_Element):

    def __init__(self, tag, text):
        super().__init__(tag)
        if isinstance(text, TextConstruct):
            self.text = text.text
            self.set('type', text.type)
        else:
            self.text = text


class _DateElement(_Element):

    def __init__(self, tag, date: datetime.date):
        super().__init__(tag)
        self.text = date.isoformat()


ID = functools.partial(_TextElement, 'id')
Title = functools.partial(_TextElement, 'title')
Rights = functools.partial(_TextElement, 'rights')
Name = functools.partial(_TextElement, 'name')
Summary = functools.partial(_TextElement, 'summary')
URI = functools.partial(_TextElement, 'uri')
Email = functools.partial(_TextElement, 'email')

Published = functools.partial(_DateElement, 'published')
Updated = functools.partial(_DateElement, 'updated')

TextConstruct = collections.namedtuple('TextConstruct', 'text type')
