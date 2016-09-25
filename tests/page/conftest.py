import pytest

from mir.frelia.document import Document


@pytest.fixture
def simple_document_renderer():
    def renderer(document):
        return document.body
    return renderer


@pytest.fixture
def simple_document_reader():
    def reader(file):
        text = file.read()
        return Document({}, text)
    return reader
