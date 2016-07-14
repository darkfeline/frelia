from unittest import mock

import frelia.transforms.document as document_transforms


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
