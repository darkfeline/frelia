from unittest import mock

import frelia.page


def test_page_renderer(document_renderer, page):
    assert page.rendered_output is None
    renderer = frelia.page.PageRenderer(document_renderer)
    renderer(page)
    assert page.rendered_output == 'rendered content'
    assert document_renderer.mock_calls == [mock.call.render(page.document)]
