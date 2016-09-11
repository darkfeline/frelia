import pytest

from mir.frelia.document import document as base
import mir.frelia.page


@pytest.fixture
def document():
    return base.Document({'sophie': 'prachta'}, 'girl meets girl')


@pytest.fixture
def page(document):
    return mir.frelia.page.Page('blog/page', document)
