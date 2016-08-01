from unittest import mock

import frelia.transforms.generic as generic_transforms


def test_compose_transforms():
    mock_func = mock.Mock()
    transform = generic_transforms.ComposeTransforms([mock_func])
    transform([mock.sentinel.object])
    assert mock_func.mock_calls == [mock.call([mock.sentinel.object])]
