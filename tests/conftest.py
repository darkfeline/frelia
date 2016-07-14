import pytest

import frelia.document
import frelia.page


@pytest.fixture
def document():
    return frelia.document.Document({'sophie': 'prachta'}, 'girl meets girl')


@pytest.fixture
def page(document):
    return frelia.page.Page('blog/page', document)
