import mir.frelia.fs as fslib
import mir.frelia.enja as enja


class _RecursiveLoader:

    def __init__(self, page_loader):
        self._page_loader = page_loader

    def __call__(self, rootdir):
        for filepath in fslib.find_files(rootdir):
            yield self._loader(filepath)


class _PageLoader:

    def __init__(self, page_class, document_class):
        self._page_class = page_class
        self._document_class = document_class

    def __call__(self, filepath):
        with open(filepath) as file:
            document = self._document_class.load(file)
        page = self._page_class.from_document(filepath, document)
        return page


class Page:

    def __init__(self, path, content):
        self.path = path
        self.content = content

    @classmethod
    def from_document(cls, path, document):
        page = cls(path, document.body)
        return page


load_pages = _RecursiveLoader(_PageLoader(Page, enja.Document))
