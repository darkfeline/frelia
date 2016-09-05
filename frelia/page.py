"""frelia page module.

Pages are an abstraction to simplify rendering of static webpages.

Pages are loaded using PageLoader, rendered using PageRenderer, and written to
files using PageWriter.

Pages have path and document attributes.  The path indicates where the page
will be written, and the actual rendering of the page is handled by the
document.

"""

import os

import frelia.fs


class Page:

    """Represents a page resource for rendering.

    Contains the page itself and the path where the page would be built.

    The rendered_output attribute caches the rendered form of the page's
    document.

    """

    def __init__(self, path, document):
        self.path = path
        self.document = document
        self.rendered_output = None

    def __repr__(self):
        return '{cls}({path!r}, {document!r})'.format(
            cls=type(self).__name__,
            path=self.path,
            document=self.document)


class PageLoader:

    """Page loader.

    Loads pages from a directory.

    """

    def __init__(self, document_reader):
        self.document_reader = document_reader

    def __call__(self, rootdir):
        """Generate PageResource instances from a directory tree."""
        document_reader = self.document_reader
        for filepath in frelia.fs.find_files(rootdir):
            with open(filepath) as file:
                document = document_reader(file)
            yield Page(filepath, document)


class PageWriter:

    """Contains logic for writing rendered pages."""

    def __init__(self, target_dir):
        self.target_dir = target_dir

    def __call__(self, pages):
        target_dir = self.target_dir
        for page in pages:
            if page.rendered_output is None:
                continue
            dst = os.path.join(target_dir, page.path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'w') as file:
                file.write(page.rendered_output)


class PageRenderer:

    """Contains logic for rendering pages."""

    def __init__(self, document_renderer):
        self.document_renderer = document_renderer

    def __call__(self, pages):
        document_renderer = self.document_renderer
        for page in pages:
            rendered_output = document_renderer(page.document)
            page.rendered_output = rendered_output
