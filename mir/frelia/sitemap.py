"""Sitemap generator.

http://www.sitemaps.org/protocol.html
"""

import datetime
import io
import numbers
import xml.etree.ElementTree as ET


class URL:

    """Sitemap URL."""

    __slots__ = ('loc', '_lastmod', '_changefreq', '_priority')

    def __init__(self, loc):
        self.loc = loc
        self.lastmod = None
        self.changefreq = None
        self.priority = None

    def __repr__(self):
        return ('<{cls} with loc={this.loc!r}, lastmod={this.lastmod!r},'
                ' changefreq={this.changefreq!r}, priority={this.priority!r}>'
                .format(cls=type(self).__qualname__, this=self))

    def to_etree(self):
        """Return etree XML representation of the URL."""
        entry = ET.Element('url')
        ET.SubElement(entry, 'loc').text = self.loc
        if self.lastmod is not None:
            ET.SubElement(entry, 'lastmod').text = self.lastmod.isoformat()
        if self.changefreq is not None:
            ET.SubElement(entry, 'changefreq').text = self.changefreq
        if self.priority is not None:
            ET.SubElement(entry, 'priority').text = str(self.priority)
        return entry

    @property
    def lastmod(self):
        return self._lastmod

    @lastmod.setter
    def lastmod(self, value):
        if self._valid_lastmod(value):
            self._lastmod = value
        else:
            raise ValidationError('lastmod must be a date or datetime.')

    def _valid_lastmod(self, value):
        return isinstance(value, (datetime.date, type(None)))

    @property
    def changefreq(self):
        return self._changefreq

    @changefreq.setter
    def changefreq(self, value):
        if value in self._VALID_CHANGEFREQ:
            self._changefreq = value
        else:
            raise ValidationError(
                'changefreq must be one of: '
                + ', '.join(repr(value) for value in self._VALID_CHANGEFREQ))

    _VALID_CHANGEFREQ = frozenset((
        None,
        'always',
        'hourly',
        'daily',
        'weekly',
        'monthly',
        'yearly',
        'never',
    ))

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if self._valid_priority(value):
            self._priority = value
        else:
            raise ValidationError(
                'priority must be a float between 0.0 and 1.0.')

    def _valid_priority(self, value):
        return value is None or (
            isinstance(value, numbers.Real)
            and 0 <= value <= 1)


def write_sitemap_urlset(file: io.TextIOBase, urls):
    """Write sitemap urlset to a file.

    urls is an iterable of URL instances.  file is a text file for writing.
    """
    urlset = ET.Element('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': ' '.join((
            'http://www.sitemaps.org/schemas/sitemap/0.9',
            'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')),
    })
    urlset.extend(url.to_etree() for url in urls)
    document = ET.ElementTree(urlset)
    document.write(file, encoding='unicode', xml_declaration=True)


class ValidationError(Exception):
    """Sitemap validation error."""
