import datetime
from unittest import mock

import frelia.page
import frelia.transforms.page as page_transforms


def test_document_page_transforms(document):
    page = frelia.page.Page('foo', document)
    document_func = mock.Mock()
    page_func = page_transforms.DocumentPageTransforms([document_func])
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
    page.path = 'blog/2010/01/02/post'
    transform = page_transforms.DateFromPath('published')
    assert 'published' not in page.document.metadata
    transform([page])
    assert page.document.metadata['published'] == datetime.date(2010, 1, 2)


def test_date_from_path_with_existing_value(page):
    page.path = 'blog/2010/01/02/post'
    page.document.metadata['published'] = 1
    transform = page_transforms.DateFromPath('published')
    transform([page])
    assert page.document.metadata['published'] == 1


def test_date_from_path_too_short(page):
    page.path = 'blog/post'
    transform = page_transforms.DateFromPath('published')
    assert 'published' not in page.document.metadata
    transform([page])
    assert 'published' not in page.document.metadata


def test_date_from_path_out_of_range(page):
    page.path = 'blog/2010/13/02/post'
    transform = page_transforms.DateFromPath('published')
    assert 'published' not in page.document.metadata
    transform([page])
    assert 'published' not in page.document.metadata


def test_date_from_path_non_number(page):
    page.path = 'blog/2010/01/tag/post'
    transform = page_transforms.DateFromPath('published')
    assert 'published' not in page.document.metadata
    transform([page])
    assert 'published' not in page.document.metadata
