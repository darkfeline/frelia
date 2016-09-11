import logging

logger = logging.getLogger(__name__)


class JinjaDocumentRenderer:

    """Render documents using Jinja."""

    def __init__(self, env, default_template='base.html'):
        self.env = env
        self.default_template = default_template

    def __repr__(self):
        return (
            '{cls}(env={this.env!r},'
            ' default_template={this.default_template!r})'
            .format(cls=type(self).__name__, this=self)
        )

    def __call__(self, document):
        """Render document."""
        logger.debug('Rendering document %r with %r...', document, self)
        template = self._get_template(document)
        context = self._get_context(document)
        return template.render(context)

    @staticmethod
    def _get_context(document):
        """Get context for rendering document."""
        context = document.metadata.copy()
        context['content'] = document.content
        return context

    def _get_template(self, document):
        """Get Jinja template for document."""
        template_name = document.metadata.get('template',
                                              self.default_template)
        return self.env.get_template(template_name)
