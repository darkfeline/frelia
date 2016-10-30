import mir.frelia.enja as enja
import mir.frelia.page as pagelib

import pytest


def test_basic_page_from_document():
    document = enja.Document('Was yea ra chs hymmnos mea')
    got = pagelib.BasicPage.from_document('foo/bar', document)
    assert got.path == 'foo/bar'
    assert got.content == 'Was yea ra chs hymmnos mea'


def test_basic_page_metadata():
    page = pagelib.BasicPage(path='foo/bar', content='spam')
    assert page.metadata == {'path': 'foo/bar'}


def test_load_pages(tmpdir):
    (tmpdir / 'file').write_text('sophie: prachta\n---\nfiris')
    got = list(pagelib.load_pages(tmpdir))
    assert got == [pagelib.BasicPage()]
