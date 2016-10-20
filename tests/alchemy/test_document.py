import collections

import pytest

import mir.frelia.alchemy as alchemy
from mir.frelia.enja import Document


def test_render_template():
    document = Document({'sophie': 'prachta'}, 'hello $ion $sophie')
    alchemy.render_template(document, {'ion': 'earthes'})
    assert document.body == 'hello earthes prachta'


def test_flatten_mapping_identity():
    got = alchemy.flatten_mapping({'sophie': 'prachta'})
    assert got == {'sophie': 'prachta'}


def test_flatten_mapping():
    got = alchemy.flatten_mapping({'pairs': {'sophie': 'prachta'}})
    assert got == {'pairs_sophie': 'prachta'}


def test_render_as_template(env):
    renderer = alchemy.JinjaRenderer(env)
    doc = Document({'sophie': 'prachta'}, 'hello')
    renderer.render_as_template(doc)
    assert doc.body == "hello [('sophie', 'prachta')]"


def test_jinja_render_default_template(env):
    renderer = alchemy.JinjaRenderer(env)
    got = renderer.render(Document({'sophie': 'prachta'}, 'girl meets girl'))
    assert got == ("base.html [('content', 'girl meets girl'),"
                   " ('sophie', 'prachta')]")


def test_jinja_render_explicit_template(env):
    renderer = alchemy.JinjaRenderer(env)
    got = renderer.render(Document({'template': 'prachta.html'},
                                   'girl meets girl'))
    assert got == ("prachta.html [('content', 'girl meets girl'),"
                   " ('template', 'prachta.html')]")


def test_set_default_metadata():
    function = alchemy.SetDefaultMetadata({'firis': 'liane'})
    doc = Document({'sophie': 'prachta'}, 'hello')
    got = function([doc])
    assert list(doc.header for doc in got) \
        == [{'sophie': 'prachta', 'firis': 'liane'}]


COPY_ARGS = 'from_field,to_field,header,expected'
CopyTest = collections.namedtuple('CopyTest', COPY_ARGS)


@pytest.mark.parametrize(COPY_ARGS, [
    CopyTest(
        from_field='sophie',
        to_field='firis',
        header={'sophie': 'prachta'},
        expected={'sophie': 'prachta', 'firis': 'prachta'}),
    CopyTest(
        from_field='sophie',
        to_field='firis',
        header={'sophie': 'prachta', 'firis': 'liane'},
        expected={'sophie': 'prachta', 'firis': 'liane'}),
])
def test_copy_metadata(from_field, to_field, header, expected):
    function = alchemy.CopyMetadata(from_field=from_field, to_field=to_field)
    doc = Document(header, '')
    got = function([doc])
    assert list(doc.header for doc in got) == [expected]
