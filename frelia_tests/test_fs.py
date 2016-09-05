from collections import Counter
import os

import pytest

import frelia.fs


@pytest.fixture
def dirtree(tmpdir):
    srcdir = tmpdir.mkdir('src')

    foodir = srcdir.mkdir('foo')
    foodir.mkdir('bar')
    foodir.join('baz').write('')

    spamdir = srcdir.mkdir('spam')
    spamdir.mkdir('eggs')
    spamdir.join('bacon').write('')
    return tmpdir


def test_walk_files(dirtree):
    root = str(dirtree.join('src'))
    got = Counter(frelia.fs.walk_files(root))
    assert got == Counter(
        os.path.join(root, path)
        for path in ('foo/baz', 'spam/bacon')
    )


def _samefile(path, first, second):
    """Return True if path relative to first and second are the same file."""
    first = first.join(path)
    second = second.join(path)
    return first.samefile(second)


def test_link_files(dirtree):
    src = dirtree.join('src')
    dst = dirtree.join('dst')
    frelia.fs.link_files(str(src), str(dst))
    assert _samefile('foo/baz', src, dst)
    assert _samefile('spam/bacon', src, dst)


@pytest.mark.parametrize(
    ('path', 'expected'),
    [
        ('foo/bar/baz', ['baz', 'bar', 'foo']),
        ('/foo/bar/baz', ['baz', 'bar', 'foo', '/']),
    ])
def test_split_filenames(path, expected):
    got = list(frelia.fs.split_filenames(path))
    assert got == expected
