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

    def rebase_path(self, basepath):
        """Rebase the page's path relative to basepath."""
        self.path = os.path.relpath(self.path, basepath)

    def publish(self, dir):
        """Write the page to a file in the directory.

        The path of the file is the page's path, relative to the directory.
        """
        dst = os.path.join(dir, self.path)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'w') as file:
            file.write(self.content)


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
