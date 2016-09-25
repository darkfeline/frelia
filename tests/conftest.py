import functools
from unittest import mock

import jinja2
import pytest

# pylint: disable=redefined-outer-name


@pytest.fixture
def env():
    env = mock.create_autospec(jinja2.Environment, instance=True)
    env.get_template.side_effect = _get_template
    env.from_string.side_effect = _from_string
    return env


def _get_template(name, *args, **kwargs):
    """Fake get_template() method."""
    template = mock.create_autospec(jinja2.Template, instance=True)
    template.render.side_effect = functools.partial(_render, name)
    return template


def _render(text, context={}):
    """Fake render() method."""
    return '%s %r' % (text, sorted(context.items()))


def _from_string(source, *args, **kwargs):
    """Fake from_string() method."""
    template = mock.create_autospec(jinja2.Template, instance=True)
    template.render.side_effect = functools.partial(_render, source)
    return template
