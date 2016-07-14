"""Document transformations."""


class RenderJinja:

    """Document transform that renders document content with Jinja.

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


class SetDefaultMetadata:

    """set default values for missing document metadata."""

    def __init__(self, defaults):
        assert isinstance(defaults, dict)
        self.defaults = defaults

    def __call__(self, documents):
        defaults = self.defaults
        for document in documents:
            new_metadata = defaults.copy()
            new_metadata.update(document.metadata)
            document.metadata = new_metadata
