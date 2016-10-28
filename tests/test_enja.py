"""Tests for mir.frelia.enja module."""

import io

import pytest

import mir.frelia.enja as enja


def test_load():
    """Test parsing a simple enja document from a file."""
    file = io.StringIO('foo: bar\n---\n<p>Hello world!</p>')
    doc = enja.load(file)
    assert doc.header == {'foo': 'bar'}
    assert doc.body == '<p>Hello world!</p>'


def test_load_empty_file():
    """Test parsing an empty enja document from a file."""
    file = io.StringIO('')
    doc = enja.load(file)
    assert doc.header == {}
    assert doc.body == ''


def test_dump():
    """Test dumping an Enja document to a file."""
    document = enja.Document(header={'sophie': 'prachta'},
                             body='girl meets girl')
    file = io.StringIO()
    enja.dump(document, file)
    assert file.getvalue() == 'sophie: prachta\n---\ngirl meets girl'


def test_document_equal():
    assert (enja.Document({'sophie': 'prachta'}, 'girl meets girl')
            == enja.Document({'sophie': 'prachta'}, 'girl meets girl'))


@pytest.mark.parametrize('a,b', [
    (enja.Document({'sophie': 'prachta'}, ''),
     enja.Document({'sophie': 'prachta'}, 'girl meets girl')),
    (enja.Document({'sophie': 'prachta'}, 'girl meets girl'),
     enja.Document({}, 'girl meets girl')),
])
def test_document_unequal(a, b):
    assert a != b


def test_document_equal_nondocument():
    assert enja.Document({}, '') != object()
