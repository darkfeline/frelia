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

import collections
from collections.abc import Mapping
import datetime
import logging
import pathlib
import string

logger = logging.getLogger(__name__)


def render(page, base_mapping):
    """Render documents using Python templates.

    Python templates provide the fastest possible templating in Python and are
    significantly faster than Jinja templates.
    """
    mapping = collections.ChainMap(page.metadata, base_mapping)
    flat_mapping = _flatten_mapping(mapping)
    template = string.Template(page.content)
    return template.safe_substitute(flat_mapping)


def _flatten_mapping(mapping, separator='_', prefix=''):
    """Flatten nested mappings.

    >>> got = _flatten_mapping({'foo': {'bar': 'baz'}})
    >>> got == {'foo_bar': 'baz'}
    True
    """
    new_mapping = _prefix_keys(mapping, prefix)
    nested_mappings = _nested_mappings(mapping)
    for key, mapping in nested_mappings:
        new_items = _flatten_mapping(
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
        self._env = env
        self._default_template = default_template

    def __repr__(self):
        return ('{cls}(env={env!r}, default_template={default_template!r})'
                .format(cls=type(self).__qualname__,
                        env=self._env,
                        default_template=self._default_template))

    def render_as_template(self, document):
        """Render a document as a Jinja template.

        This allows the use of Jinja macros in the document.  Compare with
        render().

        This is extremely slow.
        """
        logger.debug('Rendering %r as template with %r.', document, self)
        document_as_template = self.env.from_string(document.content)
        context = self._get_context(document)
        return document_as_template.render(context)

    def render(self, document):
        """Render a document using Jinja."""
        logger.debug('Rendering %r with %r.', document, self)
        template = self._get_template(document)
        context = self._get_context_with_content(document)
        return template.render(context)

    def _get_context(self, document):
        """Get the context for rendering the document."""
        context = collections.ChainMap({}, document.metadata)
        return context

    def _get_context_with_content(self, document):
        context = self._get_context(document)
        context['content'] = document.content
        return context

    def _get_template(self, document):
        """Get the Jinja template for the document."""
        template_name = document.template
        return self._env.get_template(template_name)

    def _get_template_name(self, document):
        try:
            return document.template
        except AttributeError:
            return self._default_template


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
