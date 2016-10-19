"""Webpages

Pages are an abstraction to simplify rendering of static webpages.

Pages have path and document attributes.  The path indicates where the page
will be written, and the actual rendering of the page is handled by the
document.

Pages are loaded using PageLoader, rendered using PageRenderer, and written to
files using PageWriter.
"""

import os

import mir.frelia.fs


class Page:

    """Webpage defined by a path and document."""

    def __init__(self, path, document):
        self.path = path
        self.document = document

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.path == other.path and self.document == other.document
        else:
            return NotImplemented


class RenderedPage:

    """Webpage defined by a path and text."""

    def __init__(self, path, text):
        self.path = path
        self.text = text

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.path == other.path and self.text == other.text
        else:
            return NotImplemented


class PageLoader:

    """Page loader.

    Loads pages from a directory.
    """

    def __init__(self, document_reader):
        self.document_reader = document_reader

    def __call__(self, rootdir):
        """Generate PageResource instances from a directory tree."""
        document_reader = self.document_reader
        for filepath in mir.frelia.fs.find_files(rootdir):
            with open(filepath) as file:
                document = document_reader(file)
            yield Page(filepath, document)


class PageRenderer:

    """Contains logic for rendering pages."""

    def __init__(self, document_renderer):
        self.document_renderer = document_renderer

    def __call__(self, pages):
        document_renderer = self.document_renderer
        for page in pages:
            rendered_output = document_renderer(page.document)
            yield RenderedPage(page.path, rendered_output)


class PageWriter:

    """Contains logic for writing rendered pages."""

    def __init__(self, target_dir):
        self.target_dir = target_dir

    def __call__(self, rendered_pages):
        target_dir = self.target_dir
        for page in rendered_pages:
            dst = os.path.join(target_dir, page.path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'w') as file:
                file.write(page.text)
