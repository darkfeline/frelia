"""File system utilities."""

import os
import pathlib


def find_files(path):
    """Yield the paths of all files in a directory tree."""
    for dirpath, dirnames, filenames in os.walk(path):
        dirpath = pathlib.Path(dirpath)
        for filename in filenames:
            yield dirpath / filename


def link_recursively(src_dir, dst_dir):
    """Hard link files recursively from src to dst."""
    dst_dir = pathlib.Path(dst_dir)
    for filepath in find_files(src_dir):
        rel_filepath = filepath.relative_to(src_dir)
        dst_filepath = dst_dir / rel_filepath
        make_parents(dst_filepath)
        os.link(filepath, dst_filepath)


def make_parents(path):
    """Make parent directories of path."""
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
