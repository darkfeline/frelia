"""File system utilities."""

import os


def walk_files(path):
    """Generate the pathnames of all files in a directory tree."""
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def link_files(src, dst):
    """Hard link files recursively from src to dst.."""
    for src_path in walk_files(src):
        rel_path = os.path.relpath(src_path, src)
        dst_path = os.path.join(dst, rel_path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        os.link(src_path, dst_path)


def path_filenames(path):
    """Split a path and yield its filenames."""
    while path:
        path, filename = os.path.split(path)
        if filename:
            yield filename
        else:
            yield path
            break
