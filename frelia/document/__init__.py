class Document:

    """Documents with metadata.

    Documents have structured metadata and a content body, both of an
    unspecified format.

    """

    def __init__(self, metadata, content):
        self.metadata = metadata
        self.content = content

    def __repr__(self):
        return '<{cls} at 0x{id:x} with metadata {metadata!r}>'.format(
            cls=type(self).__name__,
            id=id(self),
            metadata=self.metadata)
