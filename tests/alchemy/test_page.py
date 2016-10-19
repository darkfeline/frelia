import datetime
from unittest import mock

import pytest

import mir.frelia.alchemy as alchemy
from mir.frelia.enja import Document
from mir.frelia.page import Page
from mir.frelia.page import RenderedPage


def render_doc(documents):
    """Simple document renderer."""
    for document in documents:  # pragma: no branch
        document.body = 'rendered ' + document.body
        yield document


@pytest.mark.parametrize('texts,expected', [
    (['hi'], ['rendered hi']),
    ([], []),
])
def test_lift_page(texts, expected):
    pages = [Page(mock.sentinel.dummy, Document({}, text)) for text in texts]
    page_func = alchemy.LiftPage(render_doc)
    got = page_func(pages)
    assert list(got) == [Page(mock.sentinel.dummy, Document({}, text))
                         for text in expected]


def test_rebase_page_path():
    page = Page('root/blog/post', mock.sentinel.dummy)
    transform = alchemy.RebasePagePath('root')
    got = transform([page])
    assert list(page.path for page in got) == ['blog/post']


@pytest.mark.parametrize('path,header,expected', [
    ('blog/2010/01/02/post', {}, {'published': datetime.date(2010, 1, 2)}),
    ('blog/2010/01/02/post', {'published': 1}, {'published': 1}),
    ('blog/post', {}, {}),
    ('blog/2010/13/02/post', {}, {}),
    ('blog/2010/01/tag/post', {}, {}),
])
def test_date_from_path(path, header, expected):
    page = Page(path, Document(header, ''))
    transform = alchemy.SetDateFromPath('published')
    got = transform([page])
    assert list(page.document.header for page in got) == [expected]


def test_page_equal():
    assert Page('post', 'content') == Page('post', 'content')


def test_page_unequal_wrong_type():
    assert Page('post', 'content') != object()


def test_rendered_page_equal():
    assert RenderedPage('post', 'content') == RenderedPage('post', 'content')


def test_rendered_page_unequal_wrong_type():
    assert RenderedPage('post', 'content') != object()
