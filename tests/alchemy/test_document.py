import collections
from unittest import mock

import pytest

import mir.frelia.alchemy as alchemy
from mir.frelia.document import Document


def test_render_template():
    render = alchemy.RenderTemplateDocument({'ion': 'earthes'})
    doc = Document({'sophie': 'prachta'}, 'hello $ion $sophie')
    got = render([doc])
    assert list(doc.body for doc in got) == ['hello earthes prachta']


def test_render_jinja(env):
    render = alchemy.RenderJinjaDocument(env)
    doc = Document({'sophie': 'prachta'}, 'hello')
    got = render([doc])
    assert list(doc.body for doc in got) == ["hello [('sophie', 'prachta')]"]


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
