"""Document transformations."""

import logging
import string

logger = logging.getLogger(__name__)


class RenderTemplate:

    """Document transform that renders document content using Python templates.

    This is faster than RenderJinja.

    """

    def __init__(self, mapping):
        self.mapping = mapping

    def __call__(self, documents):
        copy = self.mapping.copy
        for document in documents:
            mapping = copy()
            mapping.update(document.metadata)
            template = string.Template(document.content)
            document.content = template.safe_substitute(mapping)


class RenderJinja:

    """Document transform that renders document content with Jinja.

    This renders the document content as a Jinja template.  This allows the use
    of Jinja macros in the document, for example.

    This is extremely slow.

    """

    def __init__(self, env):
        self.env = env

    def __call__(self, documents):
        template_from_string = self.env.from_string
        for document in documents:
            logger.debug('Rendering document content for %r...', document)
            content_as_template = template_from_string(document.content)
            rendered_content = content_as_template.render(document.metadata)
            document.content = rendered_content


class SetDefaultMetadata:

    """set default values for missing document metadata."""

    def __init__(self, defaults):
        assert isinstance(defaults, dict)
        self.defaults = defaults

    def __call__(self, documents):
        make_copy = self.defaults.copy
        for document in documents:
            new_metadata = make_copy()
            new_metadata.update(document.metadata)
            document.metadata = new_metadata


class CopyMetadata:

    """Set missing metadata field with other metadata field."""

    def __init__(self, from_field, to_field):
        self.from_field = from_field
        self.to_field = to_field

    def __call__(self, documents):
        """Set index using aggregate."""
        from_field = self.from_field
        to_field = self.to_field
        for document in documents:
            metadata = document.metadata
            if to_field not in metadata and from_field in metadata:
                metadata[to_field] = metadata[from_field]
