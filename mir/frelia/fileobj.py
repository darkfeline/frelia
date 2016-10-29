import collections

import mir.frelia.fs as fslib


FileObject = collections.namedtuple('FileObject', 'path,object')


class FileObjectLoader:

    def __init__(self, loader):
        self._loader = loader

    def __call__(self, rootdir):
        loader = self._loader
        for filepath in fslib.find_files(rootdir):
            with open(filepath) as file:
                object_ = loader(file)
            yield FileObject(filepath, object_)
