"""Page transformations."""

import datetime
import itertools
import os

import frelia.fs


class DocumentPageTransform:

    """Maps a document transformation to a page transformation."""

    def __init__(self, transform):
        self.transform = transform

    def __call__(self, pages):
        self.transform(page.document for page in pages)


class RebasePagePath:

    """Page transformation that rebases page paths relative to base path."""

    def __init__(self, basepath):
        self.basepath = basepath

    def __call__(self, pages):
        basepath = self.basepath
        for page in pages:
            page.path = os.path.relpath(page.path, basepath)


def strip_page_extension(pages):
    """Conditionally strip page path filename extension.

    HTML resources that are not index.html will be stripped.

    """
    for page in pages:
        base, ext = os.path.splitext(page.path)
        strip = (
            ext == '.html'
            and os.path.basename(page.path) != 'index.html'
        )
        if strip:
            page.path = base


class DateFromPath:

    """Set metadata date from page path."""

    def __init__(self, fieldname, default=None):
        self.fieldname = fieldname
        self.default = default

    def __call__(self, pages):
        fieldname = self.fieldname
        for page in pages:
            metadata = page.document.metadata
            if fieldname not in metadata:
                metadata[fieldname] = self._parse_date_from_path(page.path)

    def _parse_date_from_path(self, path):
        path = os.path.dirname(path)
        filenames = frelia.fs.path_filenames(path)
        parts = tuple(itertools.islice(filenames, 3))
        try:
            day, month, year = parts
            return datetime.date(int(year), int(month), int(day))
        except ValueError:
            return self.default
