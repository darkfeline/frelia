"""Document transformations."""


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
