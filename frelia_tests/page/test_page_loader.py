from unittest import mock

import pytest

import mir.frelia.page


def test_load_pages(tmpdir, document_class, document):
    root = tmpdir.mkdir('root')
    filepath = root.mkdir('blog').join('post')
    filepath.write('')
    loader = mir.frelia.page.PageLoader(document_class)

    got = list(loader(str(root)))

    assert len(got) == 1
    page = got[0]
    assert page.path == str(filepath)
    assert page.document is document


@pytest.fixture
def document_class(document):
    cls = mock.Mock([])
    cls.return_value = document
    return cls
