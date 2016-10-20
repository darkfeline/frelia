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

import datetime
import itertools
import logging
import os
import string

from mir.monads.id import Identity

import mir.frelia.fs

logger = logging.getLogger(__name__)


class compose:

    """Compose transmutation functions."""

    def __init__(self, *functions):
        self.functions = functions

    def __repr__(self):
        return '{cls}({this.functions!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def __call__(self, iterable):
        """Apply all transmutation functions to objects."""
        functor = Identity(iterable)
        for function in self.functions:
            functor = functor.fmap(function)
        result_iterable, = functor
        yield from result_iterable


class RenderTemplateDocument:

    """Render documents using Python templates.

    Python templates provide the fastest possible templating in Python and are
    significantly faster than Jinja templates.
    """

    def __init__(self, mapping):
        self.mapping = _flatten_mapping(mapping)

    def __repr__(self):
        return '{cls}({this.mapping!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def __call__(self, documents):
        copy = self.mapping.copy
        for document in documents:
            mapping = copy()
            mapping.update(document.header)
            template = string.Template(document.body)
            document.body = template.safe_substitute(mapping)
            yield document


def _flatten_mapping(mapping, separator='_', prefix=''):
    """Flatten nested mappings.

    >>> got = _flatten_mapping({'foo': {'bar': 'baz'}})
    >>> got == {'foo_bar': 'baz'}
    True
    """
    if prefix:
        prefix = prefix + separator
        new_mapping = _add_prefix_to_keys(mapping, prefix)
    else:
        new_mapping = mapping.copy()
    nested_mappings = {key: value for key, value in mapping.items()
                       if isinstance(value, dict)}
    for key, value in nested_mappings.items():
        value = _flatten_mapping(
            mapping=value,
            separator=separator,
            prefix=prefix + key if prefix else key)
        new_mapping.pop(key)
        new_mapping.update(value)
    return new_mapping


def _add_prefix_to_keys(mapping, prefix):
    """Prepend a prefix to all keys in a mapping."""
    return {prefix + key: value for key, value in mapping.items()}


class JinjaRenderer:

    def __init__(self, env):
        self.env = env

    def __repr__(self):
        return '{cls}({env!r})'.format(
            cls=type(self).__qualname__, env=self.env)

    def render_as_template(self, document):
        """Render a document as a Jinja template.

        This allows the use of Jinja macros in the document.  Compare with
        jinja_render().

        This is extremely slow.
        """
        logger.debug('Rendering %r content with %r.', document, self)
        document_as_template = self.env.from_string(document.body)
        rendered_content = document_as_template.render(document.header)
        document.body = rendered_content

    def render(self, document, default_template='base.html'):
        """Render a document using Jinja."""
        logger.debug('Rendering document %r with %r.', document, self)
        template = self._get_template(document, default_template)
        context = self._get_context(document)
        return template.render(context)

    @staticmethod
    def _get_context(document):
        """Get the context for rendering the document."""
        context = document.header.copy()
        context['content'] = document.body
        return context

    def _get_template(self, document, default_template):
        """Get the Jinja template for the document."""
        template_name = document.header.get('template', default_template)
        return self.env.get_template(template_name)


class CopyMetadata:

    """Set a missing document metadata field with another metadata field."""

    def __init__(self, from_field, to_field):
        self.from_field = from_field
        self.to_field = to_field

    def __repr__(self):
        return ('{cls}(from_field={this.from_field!r},'
                ' to_field={this.to_field!r})'
                .format(
                    cls=type(self).__qualname__,
                    this=self))

    def __call__(self, documents):
        from_field = self.from_field
        to_field = self.to_field
        for document in documents:
            header = document.header
            if to_field not in header and from_field in header:
                header[to_field] = header[from_field]
            yield document


class SetDefaultMetadata:

    """Set default values for missing document metadata."""

    def __init__(self, defaults):
        assert isinstance(defaults, dict)
        self.defaults = defaults

    def __repr__(self):
        return '{cls}({this.defaults!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def __call__(self, documents):
        make_copy = self.defaults.copy
        for document in documents:
            new_header = make_copy()
            new_header.update(document.header)
            document.header = new_header
            yield document


class SetDateFromPath:

    """Set pages' date header from page path.

    Attempt to set the given header field, if missing, to a date parsed from
    the page path.
    """

    def __init__(self, fieldname):
        self.fieldname = fieldname

    def __repr__(self):
        return '{cls}({this.fieldname!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def __call__(self, pages):
        fieldname = self.fieldname
        parse_date = _parse_date_from_path
        for page in pages:
            metadata = page.content.header
            if fieldname not in metadata:
                try:
                    metadata[fieldname] = parse_date(page.path)
                except ValueError:
                    logger.exception('Could not parse date for %r', page)
            yield page


def _parse_date_from_path(path):
    """Parse a date using the final filenames in a path."""
    path = os.path.dirname(path)
    filenames = mir.frelia.fs.split_filenames(path)
    day, month, year = tuple(itertools.islice(filenames, 3))
    return datetime.date(int(year), int(month), int(day))


class RebasePagePath:

    """Rebase page paths relative to a base path."""

    def __init__(self, basepath):
        self.basepath = basepath

    def __repr__(self):
        return '{cls}({this.basepath!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def __call__(self, pages):
        basepath = self.basepath
        for page in pages:
            new_path = os.path.relpath(page.path, basepath)
            page.path = new_path
            yield page
