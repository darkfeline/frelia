import pytest

from frelia.document import base
import frelia.page


@pytest.fixture
def document():
    return base.Document({'sophie': 'prachta'}, 'girl meets girl')


@pytest.fixture
def page(document):
    return frelia.page.Page('blog/page', document)
