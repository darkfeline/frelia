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
        for filepath in frelia.fs.walk_files(root):
            yield self.load_page(filepath, root)

    def load_page(self, filepath, root=os.curdir):
        """Load a single page resource from the file system."""
        path = self._get_page_resource_path(filepath, root)
        with open(filepath) as file:
            document = self.document_reader(file)
        return Page(path, document)

    @classmethod
    def _get_page_resource_path(cls, filepath, root=os.curdir):
        """Get path of page resource loaded from file."""
        relpath = os.path.relpath(filepath, root)
        return cls._strip_extension(relpath)

    @staticmethod
    def _strip_extension(relpath):
        """Maybe strip extension from page path.

        HTML resources that are not index.html will be stripped.

        """
        base, ext = os.path.splitext(relpath)
        strip = (
            ext == '.html'
            and os.path.basename(relpath) != 'index.html'
        )
        if strip:
            return base
        else:
            return relpath


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

    def __call__(self, page):
        if page.rendered_output is None:
            return
        dst = os.path.join(self.target_dir, page.path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'w') as file:
            file.write(page.rendered_output)


class PageRenderer:

    """Contains logic for rendering pages."""

    def __init__(self, document_renderer):
        self.document_renderer = document_renderer

    def __call__(self, page):
        rendered_output = self.document_renderer(page.document)
        page.rendered_output = rendered_output
        return rendered_output
