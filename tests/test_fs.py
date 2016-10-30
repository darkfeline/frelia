import collections
import os
import pathlib

import pytest

import mir.frelia.fs as fslib


def test_find_files(tmpdir):
    (tmpdir / 'foo/bar').mkdir(parents=True)
    (tmpdir / 'foo/baz').touch()
    root = pathlib.Path(str(tmpdir))
    got = collections.Counter(fslib.find_files(root))
    assert got == collections.Counter(root / path for path in ('foo/baz',))


def test_link_recursively(tmpdir):
    (tmpdir / 'src/spam').mkdir(parents=True)
    (tmpdir / 'src/spam/eggs').touch()
    (tmpdir / 'dst').mkdir()
    fslib.link_recursively(tmpdir / 'src', tmpdir / 'dst')
    assert (tmpdir / 'src/spam/eggs').samefile(tmpdir / 'dst/spam/eggs')


def test_make_parents(tmpdir):
    fslib.make_parents(tmpdir / 'spam/eggs/ham')
    assert (tmpdir / 'spam/eggs').is_dir()
    assert not (tmpdir / 'spam/eggs/ham').exists()
