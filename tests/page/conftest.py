from unittest import mock

import pytest

import frelia.page


@pytest.fixture
def page(document):
    return frelia.page.Page('blog/page', document)


@pytest.fixture
def document_renderer():
    renderer = mock.Mock([])
    renderer.return_value = 'rendered content'
    return renderer
