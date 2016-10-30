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
    document = enja.Document('girl meets girl')
    document.header['sophie'] = 'prachta'
    file = io.StringIO()
    enja.dump(document, file)
    assert file.getvalue() == 'sophie: prachta\n---\ngirl meets girl'


def test_document_equal():
    """Test document equality."""
    doc1 = enja.Document('girl meets girl')
    doc1.header['sophie'] = 'prachta'
    doc2 = enja.Document('girl meets girl')
    doc2.header['sophie'] = 'prachta'
    assert doc1 == doc2


def test_document_unequal_body():
    """Test document with unequal body."""
    doc1 = enja.Document('girl meets girl')
    doc1.header['sophie'] = 'prachta'
    doc2 = enja.Document('')
    doc2.header['sophie'] = 'prachta'
    assert doc1 != doc2


def test_document_unequal_header():
    """Test document with unequal header."""
    doc1 = enja.Document('girl meets girl')
    doc1.header['sophie'] = 'prachta'
    doc2 = enja.Document('girl meets girl')
    assert doc1 != doc2


def test_document_unequal_type():
    """Test document against unequal type."""
    doc = enja.Document('girl meets girl')
    doc.header['sophie'] = 'prachta'
    assert doc != 'girl meets girl'


def test_document_repr():
    """Test document repr()."""
    doc = enja.Document('girl meets girl')
    doc.header['sophie'] = 'prachta'
    assert repr(doc) == "<Document with header={'sophie': 'prachta'}, body='girl meets girl'>"
