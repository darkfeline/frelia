"""Transformations.

Transformations are functions that mutate objects.

"""

import os.path


class TransformGroup:

    """Groups transformation functions."""

    def __init__(self, transforms=()):
        self.transforms = list(transforms)

    def __call__(self, iterable):
        """Apply all transformation functions to objects."""
        iterable = list(iterable)
        for transform in self.transforms:
            transform(iterable)


class DocumentPageTransform:

    """Maps a document transformation to a page transformation."""

    def __init__(self, transform):
        self.transform = transform

    def __call__(self, pages):
        self.transform(page.document for page in pages)


class RenderJinja:

    """Document transformation callable that renders document content.

    This renders the document content as a Jinja template.  This allows the use
    of Jinja macros in the document, for example.

    """

    def __init__(self, env):
        self.env = env

    def __call__(self, documents):
        env = self.env
        for document in documents:
            content_as_template = env.from_string(document.content)
            rendered_content = content_as_template.render(document.metadata)
            document.content = rendered_content


class RebasePagePath:

    """Page transformation that rebases page paths relative to directory."""

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
