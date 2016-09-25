import pytest

from mir.frelia.document import Document
import mir.frelia.page as page_mod


@pytest.mark.parametrize('page,expected', [
    (page_mod.Page('foo/bar', Document({}, 'hi')),
     [page_mod.RenderedPage('foo/bar', 'hi')]),
])
def test_page_renderer(simple_document_renderer, page, expected):
    renderer = page_mod.PageRenderer(simple_document_renderer)
    rendered_pages = renderer([page])
    assert list(rendered_pages) == expected
