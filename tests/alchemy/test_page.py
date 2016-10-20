import datetime
from unittest import mock

import pytest

import mir.frelia.alchemy as alchemy
from mir.frelia.enja import Document
from mir.frelia.page import Page


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
    assert list(page.content.header for page in got) == [expected]


def test_page_equal():
    assert Page('post', 'content') == Page('post', 'content')


def test_page_unequal_wrong_type():
    assert Page('post', 'content') != object()
