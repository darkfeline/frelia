import pytest

import mir.frelia.enja as enja


@pytest.fixture
def simple_document_renderer():
    def renderer(document):
        return document.body
    return renderer


@pytest.fixture
def simple_document_reader():
    def reader(file):
        text = file.read()
        return enja.Document({}, text)
    return reader
