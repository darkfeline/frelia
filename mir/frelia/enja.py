"""Enja document format.

Enja is a file format for storing documents in files.  This module implements
reading and writing the Enja file format.

An Enja file is a text file that contains:

- the document header metadata formatted in YAML
- a line containing three (3) hyphen-minus characters (U+002D) terminated by a
  newline character (U+000A).
- the document body
"""

import io

import yaml


class Document:

    __slots__ = ('header', 'body')

    def __init__(self, body: str):
        self.header = {}
        self.body = body

    def __repr__(self):
        return '<{cls} with header={header!r}, body={body!r}>'.format(
            cls=type(self).__qualname__,
            header=self.header,
            body=self.body,
        )

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.header == other.header and self.body == other.body)
        else:
            return NotImplemented


def dump(document, file):
    """Write a document to an enja file."""
    yaml.dump(
        document.header, file,
        Dumper=yaml.CDumper,
        default_flow_style=False)
    file.write(_DIVIDER)
    file.write(document.body)


class Loader:

    def __init__(self, document_class):
        self._document_class = document_class

    def __call__(self, file):
        """Load a document from an Enja file."""
        header_stream, file = _create_header_stream(file)
        header = _load_header(header_stream)
        body = file.read()
        document = self._document_class(body)
        document.header = header
        return document


load = Loader(Document)


_DIVIDER = '---\n'


def _create_header_stream(file):
    """Create metadata stream from a file object.

    Read off the header section from a file object and return that stream
    along with the file object, whose position will be at the start of the
    document body.
    """
    assert isinstance(file, io.TextIOBase)
    header_stream = io.StringIO()
    for line in file:
        if line == _DIVIDER:
            break
        else:
            header_stream.write(line)
    header_stream.seek(0)
    return header_stream, file


def _load_header(stream):
    header = yaml.load(stream, Loader=yaml.CLoader)
    if header is None:
        return {}
    else:
        return header
