class Document:

    """Documents with metadata.

    Documents have structured metadata and a content body, both of an
    unspecified format.

    """

    def __init__(self, metadata, content):
        self.metadata = metadata
        self.content = content

    def __repr__(self):
        return '{cls}({metadata!r}, {content!r})'.format(
            cls=type(self).__name__,
            metadata=self.metadata,
            content=self.content)
