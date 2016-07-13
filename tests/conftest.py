import pytest

import frelia.document.base


@pytest.fixture
def document():
    return frelia.document.base.Document({'sophie': 'prachta'}, 'girl meets girl')
