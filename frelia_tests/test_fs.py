import collections
import os

import pytest

import frelia.fs


def test_find_files(tmpdir):
    tmpdir.ensure_dir('foo/bar')
    tmpdir.join('foo/baz').write('')
    tmpdir.ensure_dir('spam/eggs')
    tmpdir.join('spam/bacon').write('')
    root = str(tmpdir)
    got = collections.Counter(frelia.fs.find_files(root))
    assert got == collections.Counter(
        os.path.join(root, path)
        for path in ('foo/baz', 'spam/bacon')
    )


def _assert_samefile(path, first, second):
    """Assert path relative to first and second are the same file."""
    first = first.join(path)
    second = second.join(path)
    assert first.samefile(second)


def test_link_files(tmpdir):
    src = tmpdir.mkdir('src')
    src.join('foo/baz').write('', ensure=True)
    src.join('spam/bacon').write('', ensure=True)
    dst = tmpdir.join('dst')
    frelia.fs.link_files(str(src), str(dst))
    _assert_samefile('foo/baz', src, dst)
    _assert_samefile('spam/bacon', src, dst)


@pytest.mark.parametrize(
    ('path', 'expected'),
    [
        ('foo/bar/baz', ['baz', 'bar', 'foo']),
        ('/foo/bar/baz', ['baz', 'bar', 'foo', '/']),
    ])
def test_split_filenames(path, expected):
    got = list(frelia.fs.split_filenames(path))
    assert got == expected
