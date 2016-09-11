"""Enja formatted documents.

This module implements reading and writing the enja file format.

An enja document file is a text file that contains YAML formatted metadata
separated from the succeeding document content by a line containing three
hyphen-minus characters (U+002D).

"""

import abc
import io

import yaml

from mir.frelia.document import document


class BaseLoader(abc.ABC):

    """Abstract loader for enja formatted documents.

    Concrete subclasses must implement get_document_class().

    """

    @abc.abstractmethod
    def get_document_class(self, metadata, content):
        """Get document class to use for given metadata and content.

        This method should return a subclass of Document.

        """
        raise NotImplementedError

    def __call__(self, file):
        """Load a document from an enja file."""
        metadata_stream, file = _create_metadata_stream(file)
        metadata = yaml.load(metadata_stream, Loader=yaml.CLoader)
        content = file.read()
        document_class = self.get_document_class(metadata, content)
        return document_class(metadata, content)


class Loader(BaseLoader):

    """Basic loader that only loads plain Document instances."""

    def get_document_class(self, metadata, content):
        return document.Document


def dump(doc, file):
    """Write a document to an enja file."""
    yaml.dump(
        doc.metadata,
        file,
        Dumper=yaml.CDumper,
        default_flow_style=False)
    file.write('---\n')
    file.write(doc.content)


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
