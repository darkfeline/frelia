"""Sitemap generator.

http://www.sitemaps.org/protocol.html
"""

import collections
import datetime
import io
import numbers
import xml.etree.ElementTree as ET


URL = collections.namedtuple('URL', 'loc,lastmod,changefreq,priority')


class URL:

    """Sitemap URL."""

    def __init__(self, loc, lastmod=None, changefreq=None, priority=None):
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority
        self.validate()

    def __repr__(self):
        return ('{cls}(loc={this.loc!r}, lastmod={this.lastmod!r}),'
                ' changefreq={this.changefreq!r}, priority={this.priority!r})'
                .format(cls=type(self).__qualname__, this=self))

    def to_xml(self):
        """Return ElementTree representation."""
        entry = ET.Element('url')
        ET.SubElement(entry, 'loc').text = self.loc
        if self.lastmod is not None:
            ET.SubElement(entry, 'lastmod').text = self.lastmod.isoformat()
        if self.changefreq is not None:
            ET.SubElement(entry, 'changefreq').text = self.changefreq
        if self.priority is not None:
            ET.SubElement(entry, 'priority').text = str(self.priority)
        return entry

    def validate(self):
        """Validate URL attributes.

        Raises ValidationError if an attribute is invalid.
        """
        self._validate_lastmod()
        self._validate_changefreq()
        self._validate_priority()

    def _validate_lastmod(self):
        bad = (
            self.lastmod is not None
            and not isinstance(self.lastmod, datetime.date))
        if bad:
            raise ValidationError('lastmod must be a date or datetime.')

    _VALID_CHANGEFREQ = [
        'always',
        'hourly',
        'daily',
        'weekly',
        'monthly',
        'yearly',
        'never',
    ]

    def _validate_changefreq(self):
        bad = (
            self.changefreq is not None
            and self.changefreq not in self._VALID_CHANGEFREQ)
        if bad:
            raise ValidationError('changefreq must be one of a few valid values.')

    def _validate_priority(self):
        bad = (
            self.priority is not None
            and not (
                isinstance(self.priority, numbers.Real)
                and 0 <= self.priority <= 1))
        if bad:
            raise ValidationError('priority must be a float between 0.0 and 1.0.')


def render(file: io.TextIOBase, urls):
    """Render sitemap.xml content using provided URLs.

    urls is an iterable of URL instances.  file is a text file for writing.
    """
    urlset = ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': ' '.join((
            'http://www.sitemaps.org/schemas/sitemap/0.9',
            'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')),
    })
    urlset.extend(url.to_xml() for url in urls)
    document = ET.ElementTree(urlset)
    document.write(file, encoding='unicode', xml_declaration=True)


class ValidationError(Exception): pass
