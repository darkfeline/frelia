import collections

import pytest

import mir.frelia.alchemy as alchemy


COMPOSE_ARGS = 'funcs,iterable,expected'
ComposeTest = collections.namedtuple('ComposeTest', COMPOSE_ARGS)


@pytest.mark.parametrize(COMPOSE_ARGS, [
    ComposeTest(
        funcs=[lambda x: [x * 2 for x in x],
               lambda x: [x + 1 for x in x]],
        iterable=[1, 2],
        expected=[3, 5]),
])
def test_compose(funcs, iterable, expected):
    got = alchemy.compose(*funcs)(iterable)
    assert list(got) == expected
