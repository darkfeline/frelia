from unittest import mock

import frelia.transforms.document as document_transforms


def test_render_template(document):
    render = document_transforms.RenderTemplate({'ion': 'earthes'})
    document.content = 'hello $ion'
    render([document])
    assert document.content == 'hello earthes'


def test_render_jinja(env, template, document):
    render = document_transforms.RenderJinja(env)
    assert document.content != 'rendered template'
    render([document])
    assert document.content == 'rendered template'
    assert template.mock_calls == [mock.call.render(document.metadata)]


def test_set_default_metadata(document):
    transform = document_transforms.SetDefaultMetadata({'firis': 'liane'})
    assert document.metadata == {'sophie': 'prachta'}
    transform([document])
    assert document.metadata == {'sophie': 'prachta', 'firis': 'liane'}


def test_copy_metadata(document):
    transform = document_transforms.CopyMetadata('sophie', 'firis')
    assert document.metadata == {'sophie': 'prachta'}
    transform([document])
    assert document.metadata == {'sophie': 'prachta', 'firis': 'prachta'}


def test_copy_metadata_with_existing_value(document):
    transform = document_transforms.CopyMetadata('sophie', 'firis')
    document.metadata = {'sophie': 'prachta', 'firis': 'liane'}
    transform([document])
    assert document.metadata == {'sophie': 'prachta', 'firis': 'liane'}
