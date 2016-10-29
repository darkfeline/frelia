"""File system utilities."""

import os


def find_files(path):
    """Yield the paths of all files in a directory tree."""
    for dirpath, dirnames, filenames in os.walk(path):
        del dirnames
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def link_recursively(src_dir, dst_dir):
    """Hard link files recursively from src to dst."""
    for filepath in find_files(src_dir):
        rel_filepath = os.path.relpath(filepath, src_dir)
        dst_filepath = os.path.join(dst_dir, rel_filepath)
        link_parents(filepath, dst_filepath)


def link_parents(src, dst):
    """Link src to dst, creating  parent directories."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    os.link(src, dst)


def write_parents(path, string):
    """Write string to file at path, creating parent directories."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        file.write(string)
