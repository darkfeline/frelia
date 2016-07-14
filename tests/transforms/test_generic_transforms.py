from unittest import mock

import frelia.transforms.generic as generic_transforms


def test_transform_group():
    mock_func = mock.Mock()
    transform = generic_transforms.TransformGroup([mock_func])
    transform([mock.sentinel.object])
    assert mock_func.mock_calls == [mock.call([mock.sentinel.object])]
