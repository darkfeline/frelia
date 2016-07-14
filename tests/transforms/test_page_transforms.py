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
