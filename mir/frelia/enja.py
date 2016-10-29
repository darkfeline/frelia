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

    _DIVIDER = '---\n'

    def __init__(self, body: str):
        self.header = {}
        self.body = body

    @classmethod
    def load(cls, file):
        """Load a document from an Enja file."""
        header_stream, file = cls._create_header_stream(file)
        header = cls._load_header(header_stream)
        body = file.read()
        return Document(header, body)

    def dump(self, file):
        """Write a document to an enja file."""
        yaml.dump(
            self.header, file,
            Dumper=yaml.CDumper,
            default_flow_style=False)
        file.write(self._DIVIDER)
        file.write(self.body)

    @classmethod
    def _create_header_stream(cls, file):
        """Create metadata stream from a file object.

        Read off the header section from a file object and return that stream
        along with the file object, whose position will be at the start of the
        document body.
        """
        assert isinstance(file, io.TextIOBase)
        header_stream = io.StringIO()
        for line in file:
            if line == cls._DIVIDER:
                break
            else:
                header_stream.write(line)
        header_stream.seek(0)
        return header_stream, file

    @staticmethod
    def _load_header(stream):
        header = yaml.load(stream, Loader=yaml.CLoader)
        if header is None:
            return {}
        else:
            return header
