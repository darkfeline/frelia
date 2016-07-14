"""Document transformations."""

import logging

logger = logging.getLogger(__name__)


class RenderJinja:

    """Document transform that renders document content with Jinja.

    This renders the document content as a Jinja template.  This allows the use
    of Jinja macros in the document, for example.

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
