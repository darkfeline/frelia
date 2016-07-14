import datetime
from unittest import mock

import frelia.page
import frelia.transforms.page as page_transforms


def test_document_page_transform(document):
    page = frelia.page.Page('foo', document)
    document_func = mock.Mock()
    page_func = page_transforms.DocumentPageTransform(document_func)
    page_func([page])
    positional_args = document_func.call_args[0]
    assert list(positional_args[0]) == [document]


def test_rebase_page_path(page):
    page.path = 'root/blog/post'
    transform = page_transforms.RebasePagePath('root')
    transform([page])
    assert page.path == 'blog/post'


def test_strip_page_extension_path_html(page):
    page.path = 'blog/post.html'
    page_transforms.strip_page_extension([page])
    assert page.path == 'blog/post'


def test_strip_page_extension_path_index_html(page):
    page.path = 'blog/index.html'
    page_transforms.strip_page_extension([page])
    assert page.path == 'blog/index.html'


def test_strip_page_extension_path_nonhtml(page):
    page.path = 'static/style.css'
    page_transforms.strip_page_extension([page])
    assert page.path == 'static/style.css'


def test_date_from_path(page):
    page.path = 'blog/2010/01/02/page'
    transform = page_transforms.DateFromPath('published')
    assert page.document.metadata == {'sophie': 'prachta'}
    transform([page])
    assert page.document.metadata == {
        'sophie': 'prachta',
        'published': datetime.date(2010, 1, 2),
    }


def test_date_from_path_with_existing_value(page):
    page.path = 'blog/2010/01/02/page'
    page.document.metadata = {'published': 1}
    transform = page_transforms.DateFromPath('published')
    transform([page])
    assert page.document.metadata == {'published': 1}


def test_parse_date():
    got = page_transforms.DateFromPath._parse_date('2010', '1', '2')
    assert got == datetime.date(2010, 1, 2)


def test_parse_date_out_of_range():
    got = page_transforms.DateFromPath._parse_date('2010', '13', '2')
    assert got is None


def test_parse_date_non_number():
    got = page_transforms.DateFromPath._parse_date('frelia', '1', '2')
    assert got is None
