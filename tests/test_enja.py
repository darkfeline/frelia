"""Tests for mir.frelia.enja module."""

import io

import pytest

import mir.frelia.enja as enja
from mir.frelia.document import Document


@pytest.mark.parametrize('text,header,body', [
    ('foo: bar\n---\n<p>Hello world!</p>',
     {'foo': 'bar'}, '<p>Hello world!</p>'),
])
def test_load(text, header, body):
    """Test parsing a simple enja document from a file."""
    file = io.StringIO(text)
    loader = enja.Loader()
    doc = loader(file)
    assert doc.header == header
    assert doc.body == body


@pytest.mark.parametrize('document,text', [
    (Document({'sophie': 'prachta'}, 'girl meets girl'),
     'sophie: prachta\n---\ngirl meets girl'),
])
def test_dump(document, text):
    """Test parsing a simple enja document from a file."""
    file = io.StringIO()
    enja.dump(document, file)
    assert file.getvalue() == text
