from unittest import mock

import pytest


@pytest.fixture
def document_renderer():
    renderer = mock.Mock([])
    renderer.return_value = 'rendered content'
    return renderer
