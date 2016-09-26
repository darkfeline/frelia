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

from mir.frelia.document import Document

_DIVIDER = '---\n'


class Loader:

    """Loader for Enja formatted documents."""

    def __call__(self, file):
        """Load a document from an Enja file."""
        header_stream, file = _create_header_stream(file)
        header = yaml.load(header_stream, Loader=yaml.CLoader)
        body = file.read()
        return Document({} if header is None else header, body)


def dump(doc, file):
    """Write a document to an enja file."""
    yaml.dump(
        doc.header,
        file,
        Dumper=yaml.CDumper,
        default_flow_style=False)
    file.write(_DIVIDER)
    file.write(doc.body)


def _create_header_stream(file):
    """Create metadata stream from a file object.

    Read off the header section from a file object and return that stream along
    with the file object, whose position will be at the start of the document
    body.
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
