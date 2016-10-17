import collections

import pytest

from mir.frelia.enja import Document
import mir.frelia.renderers as renderers

RenderTest = collections.namedtuple('RenderTest', 'document,expected')


@pytest.mark.parametrize('document,expected', [
    RenderTest(
        document=Document({'sophie': 'prachta'}, 'girl meets girl'),
        expected=
        "base.html ["
        "('content', 'girl meets girl'),"
        " ('sophie', 'prachta')"
        "]"),
    RenderTest(
        document=Document({'template': 'explicit.html'}, 'girl meets girl'),
        expected=
        "explicit.html ["
        "('content', 'girl meets girl'),"
        " ('template', 'explicit.html')"
        "]"),
])
def test_render(env, document, expected):
    renderer = renderers.JinjaDocumentRenderer(env)
    got = renderer(document)
    assert got == expected
