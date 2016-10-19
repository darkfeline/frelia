"""Webpages.

Pages are an abstraction to simplify rendering of static webpages.

Pages are loaded using PageLoader, rendered using PageRenderer, and written to
files using PageWriter.
"""

import functools
import os

import mir.frelia.fs


class Page:

    """Webpage defined by a path and content.

    content can be a text string, a Document instance, or anything else to
    represent the content of a page during a stage of rendering.
    """

    def __init__(self, path, content):
        self.path = path
        self.content = content

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.path == other.path and self.content == other.content
        else:
            return NotImplemented


class BasePageLoader:

    """Page loader.

    Loads pages from a directory.
    """

    def __init__(self, page_class, loader):
        self.page_class = page_class
        self.loader = loader

    def __call__(self, rootdir):
        """Generate Page instances from a directory tree."""
        page_class = self.page_class
        loader = self.loader
        for filepath in mir.frelia.fs.find_files(rootdir):
            with open(filepath) as file:
                content = loader(file)
            yield page_class(filepath, content)


PageLoader = functools.partial(BasePageLoader, Page)


class PageRenderer:

    """Render page content using an arbitrary renderer function."""

    def __init__(self, renderer):
        self.renderer = renderer

    def __call__(self, pages):
        renderer = self.renderer
        for page in pages:
            rendered_content = renderer(page.content)
            page.content = rendered_content
            yield page


class PageWriter:

    """Write pages to files."""

    def __init__(self, target_dir):
        self.target_dir = target_dir

    def __call__(self, pages):
        target_dir = self.target_dir
        for page in pages:
            dst = os.path.join(target_dir, page.path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'w') as file:
                file.write(page.content)
