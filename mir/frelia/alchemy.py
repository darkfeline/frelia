"""Bulk transmutations

Transmutations are functions that mutate the objects in an iterable.  This
module is included in the frelia package because rendering a static site can
involve many processing steps over many pages.  By using the concept of
transmutations, these processes can be more easily organized.

By moving function calls and attribute lookups out of the loops, transmutations
also run significantly faster than a more straightforward implementation.

Transmutations should:

- accept an iterable of objects.
- do attribute lookups outside of the iterable loop.
- bind used objects to a local variable.
- return a generator of the results.
- may or may not mutate the objects in place.
"""

from collections.abc import Mapping
import datetime
import itertools
import logging
import os
import pathlib
import string

import mir.frelia.fs

logger = logging.getLogger(__name__)


def render_template(document, mapping):
    """Render documents using Python templates.

    Python templates provide the fastest possible templating in Python and are
    significantly faster than Jinja templates.
    """
    mapping = mapping.copy()
    mapping.update(document.header)
    template = string.Template(document.body)
    document.body = template.safe_substitute(mapping)


def flatten_mapping(mapping, separator='_', prefix=''):
    """Flatten nested mappings.

    >>> got = flatten_mapping({'foo': {'bar': 'baz'}})
    >>> got == {'foo_bar': 'baz'}
    True
    """
    new_mapping = _prefix_keys(mapping, prefix)
    nested_mappings = _nested_mappings(mapping)
    for key, mapping in nested_mappings:
        new_items = flatten_mapping(
            mapping=mapping,
            separator=separator,
            prefix=prefix + key + separator)
        new_mapping.pop(key)
        new_mapping.update(new_items)
    return new_mapping


def _prefix_keys(mapping, prefix):
    """Prepend a prefix to all keys in a mapping."""
    return {prefix + key: value for key, value in mapping.items()}


def _nested_mappings(mapping):
    return ((key, value) for key, value in mapping.items()
            if isinstance(value, Mapping))


class JinjaRenderer:

    def __init__(self, env, default_template='base.html'):
        self.env = env
        self.default_template = default_template

    def __repr__(self):
        return '{cls}({env!r})'.format(
            cls=type(self).__qualname__, env=self.env)

    def render_as_template(self, document):
        """Render a document as a Jinja template.

        This allows the use of Jinja macros in the document.  Compare with
        render().

        This is extremely slow.
        """
        logger.debug('Rendering %r content with %r.', document, self)
        document_as_template = self.env.from_string(document.body)
        rendered_body = document_as_template.render(document.header)
        document.body = rendered_body

    def render(self, document):
        """Render a document using Jinja."""
        logger.debug('Rendering document %r with %r.', document, self)
        template = self._get_template(document)
        context = self._get_context(document)
        rendered_body = template.render(context)
        document.body = rendered_body

    def _get_context(self, document):
        """Get the context for rendering the document."""
        context = document.header.copy()
        context['content'] = document.body
        return context

    def _get_template(self, document):
        """Get the Jinja template for the document."""
        template_name = document.header.get('template', self.default_template)
        return self.env.get_template(template_name)


def parse_date_from_path(path):
    """Parse a date using the final filenames in a path."""
    path = pathlib.Path(path)
    for year, month, day in _iter_candidate_parts(path):
        try:
            return datetime.date(int(year), int(month), int(day))
        except ValueError:
            continue
    else:
        raise ValueError("%r doesn't contain date" % path)


def _iter_candidate_parts(path):
    """Generate candidate date parts from path.

            blog/2016/01/02/posts
    yields:           y   m   d
    yields:       y   m   d
    yields:  y    m   d
    """
    path = pathlib.Path(path)
    if len(path.parts) < 3:
        return
    reversed_parts = reversed(path.parts)
    yield from zip(
        reversed_parts[2:],
        reversed_parts[1:],
        reversed_parts)
