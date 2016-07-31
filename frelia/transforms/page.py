"""Page transformations."""

import datetime
import itertools
import logging
import os

import frelia.fs

logger = logging.getLogger(__name__)


class DocumentPageTransforms:

    """Maps document transformations to page transformations."""

    def __init__(self, transforms):
        self.transforms = list(transforms)

    def __call__(self, pages):
        documents = [page.document for page in pages]
        for transform in self.transforms:
            transform(documents)


class RebasePagePath:

    """Page transformation that rebases page paths relative to base path."""

    def __init__(self, basepath):
        self.basepath = basepath

    def __call__(self, pages):
        basepath = self.basepath
        for page in pages:
            page.path = os.path.relpath(page.path, basepath)


class StripExtensions:

    """Conditionally strip page path filename extension.

    HTML resources will have their extensions stripped, except "special" files
    like index.html or 404.html.

    """

    def __call__(self, pages):
        splitext = os.path.splitext
        basename = os.path.basename
        special = {'index.html', '404.html'}
        for page in pages:
            base, ext = splitext(page.path)
            strip = (
                ext == '.html'
                and basename(page.path) not in special
            )
            if strip:
                page.path = base


class DateFromPath:

    """Set metadata date from page path.

    Attempt to set the given metadata field, if missing, to a date parsed from
    the page path.

    """

    def __init__(self, fieldname):
        self.fieldname = fieldname

    def __call__(self, pages):
        fieldname = self.fieldname
        for page in pages:
            metadata = page.document.metadata
            if fieldname not in metadata:
                try:
                    metadata[fieldname] = self._parse_date(page.path)
                except ValueError as e:
                    logger.warning('Could not parse date for %r: %s', page, e)

    @staticmethod
    def _parse_date(path):
        path = os.path.dirname(path)
        filenames = frelia.fs.split_filenames(path)
        parts = tuple(itertools.islice(filenames, 3))
        day, month, year = parts
        return datetime.date(int(year), int(month), int(day))
