"""frelia page module.

Contains resources for loading and rendering pages.

Documents represent documents of unspecified format.  Documents have metadata
and content attributes.

Pages bind documents to paths.  Pages have path and document attributes.

Pages can be loaded from the file system using PageLoader.  You need to pass in
the document class, which is used to load documents from files.  frelia.enja
implements one such document class and file format.

Documents are rendered using a DocumentRenderer.  This transforms the
document's content and metadata into an output format.  This module implements
JinjaDocumentRenderer.  DocumentRenderers have the method render(document).

Pages are rendered using PageRenderer.  PageRenderer takes a DocumentRenderer
and renders pages by writing the document's rendered output to the file
corresponding to the page's path.

"""

import os

import frelia.descriptors
import frelia.fs


class PageLoader:

    """Page loader."""

    def __init__(self, document_reader):
        self.document_reader = document_reader

    def load_pages(self, root):
        """Generate PageResource instances from a directory tree."""
        document_reader = self.document_reader
        for filepath in frelia.fs.walk_files(root):
            with open(filepath) as file:
                document = document_reader(file)
            yield Page(filepath, document)


class Page:

    """Represents a page resource for rendering.

    Contains the page itself and the path where the page would be built.

    The rendered_output attribute caches the rendered form of the page's document.

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
