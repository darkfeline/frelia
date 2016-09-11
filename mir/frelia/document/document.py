class Document:

    """Document with metadata.

    A document has structured metadata and a content body, both in an
    unspecified format.  Basically, a document represents a UNIX file (a bag of
    bytes, or Unicode text in this case), but with metadata.

    """

    def __init__(self, metadata, content):
        self.metadata = metadata
        self.content = content

    def __repr__(self):
        return '<{cls} at 0x{id:x} with metadata {metadata!r}>'.format(
            cls=type(self).__name__,
            id=id(self),
            metadata=self.metadata)
