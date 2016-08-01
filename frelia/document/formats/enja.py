"""Enja documents.

This module implements reading and writing the enja file format.

An enja document file is a text file that contains YAML formatted metadata
separated from the succeeding document content by a line containing three
hyphen-minus characters (U+002D).

"""

import io

import yaml

from frelia.document import base


def load(file):
    """Load a document from an enja file."""
    metadata_stream, file = _create_metadata_stream(file)
    metadata = yaml.load(metadata_stream, Loader=yaml.CLoader)
    content = file.read()
    return base.Document(metadata, content)


def dump(document, file):
    """Write a document to an enja file."""
    yaml.dump(
        document.metadata,
        file,
        Dumper=yaml.CDumper,
        default_flow_style=False)
    file.write('---\n')
    file.write(document.content)


def _create_metadata_stream(file):
    """Create metadata stream from a file object.

    Read off the metadata section from a file object and return that stream
    along with the file object, whose stream position will be at the start
    of the document content.

    """
    assert isinstance(file, io.TextIOBase)
    metadata_stream = io.StringIO()
    for line in file:
        if line == '---\n':
            break
        else:
            metadata_stream.write(line)
    metadata_stream.seek(0)
    return metadata_stream, file
