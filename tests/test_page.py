import mir.frelia.enja as enja
import mir.frelia.page as page_mod

import pytest


@pytest.fixture
def simple_document_reader():
    def reader(file):
        text = file.read()
        return enja.Document({}, text)
    return reader


def test_load_pages(tmpdir, simple_document_reader):
    root = tmpdir.mkdir('root')
    filepath = root.mkdir('blog').join('post')
    filepath.write('test')
    loader = page_mod.PageLoader(simple_document_reader)

    got = list(loader(str(root)))

    assert len(got) == 1
    page = got[0]
    assert page.path == str(filepath)
    assert page.content.body == 'test'


def test_page_publish(tmpdir):
    root = tmpdir.mkdir('root')
    page = page_mod.Page('blog/post', 'foobar')
    page.publish(str(root))

    filepath = root.join('blog').join('post')
    assert filepath.read_text('utf-8') == 'foobar'
