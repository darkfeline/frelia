import pytest

import frelia.document


@pytest.fixture
def document():
    return frelia.document.Document({'sophie': 'prachta'}, 'girl meets girl')
