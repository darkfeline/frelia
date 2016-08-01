import pytest

import frelia.task


@pytest.fixture
def uni_task():
    return frelia.task.Task('uni', lambda: 'uni')


@pytest.fixture
def craft_task():
    return frelia.task.Task('craft', lambda uni: uni + ' craft', ['uni'])


@pytest.fixture
def bad_uni_task():
    return frelia.task.Task('uni', lambda craft: craft + ' uni', ['craft'])
