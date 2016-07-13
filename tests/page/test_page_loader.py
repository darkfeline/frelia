from unittest import mock

import pytest

import frelia.page


def test_load_pages(tmpdir, document_class, document):
    root = tmpdir.mkdir('root')
    filepath = root.mkdir('blog').join('post')
    filepath.write('')
    loader = frelia.page.PageLoader(document_class)

    got = list(loader.load_pages(str(root)))

    assert len(got) == 1
    page = got[0]
    assert page.path == 'blog/post'
    assert page.document == document


def test_load_page(tmpdir, document_class, document):
    root = tmpdir.mkdir('root')
    filepath = root.mkdir('blog').join('post')
    filepath.write('')
    loader = frelia.page.PageLoader(document_class)
    page = loader.load_page(str(filepath), str(root))
    assert page.document is document
    assert page.path == 'blog/post'


def test_get_page_resource_path():
    got = frelia.page.PageLoader._get_page_resource_path(
        'root/blog/post',
        'root')
    assert got == 'blog/post'


def test_strip_extension_path_html():
    got = frelia.page.PageLoader._strip_extension('blog/post.html')
    assert got == 'blog/post'


def test_strip_extension_path_index_html():
    got = frelia.page.PageLoader._strip_extension('blog/index.html')
    assert got == 'blog/index.html'


def test_strip_extension_path_nonhtml():
    got = frelia.page.PageLoader._strip_extension('static/style.css')
    assert got == 'static/style.css'


@pytest.fixture
def document_class(document):
    cls = mock.NonCallableMock(['load'])
    cls.load.return_value = document
    return cls
