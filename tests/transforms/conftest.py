
from unittest import mock

import jinja2
import pytest


@pytest.fixture
def template():
    template = mock.create_autospec(jinja2.Template, instance=True)
    template.render.return_value = 'rendered template'
    return template


@pytest.fixture
def env(template):
    env = mock.create_autospec(jinja2.Environment, instance=True)
    env.from_string.return_value = template
    return env
