import abc

import mir.frelia.fs as fslib
import mir.frelia.enja as enja


class _RecursiveLoader:

    def __init__(self, page_loader):
        self._page_loader = page_loader

    def __call__(self, rootdir):
        for filepath in fslib.find_files(rootdir):
            yield self._loader(filepath)


class _PageLoader:

    def __init__(self, page_class, document_loader):
        self._page_class = page_class
        self._document_loader = document_loader

    def __call__(self, filepath):
        with open(filepath) as file:
            document = self._document_loader(file)
        page = self._page_class.from_document(filepath, document)
        return page


class Page(abc.ABC):

    """Page interface.

    Classes should provide the following attributes:
        metadata: A mapping of the page's metadata.
        content: The page's content as a string.

    The metadata attribute does not have to be settable, but if it is settable,
    setting it should mutate the page accordingly.

    The mapping obtained from the metadata attribute should not be mutated, so
    that classes may implement the metadata attribute freely.
    """

    @classmethod
    @abc.abstractmethod
    def from_document(cls, path, document):
        """Create a page instance from a document."""
        raise NotImplementedError


class BasicPage(Page):

    def __init__(self, path, content):
        self.path = path
        self.content = content

    @classmethod
    def from_document(cls, path, document):
        page = cls(path, document.body)
        return page

    @property
    def metadata(self):
        return {
            'path': self.path,
        }


load_pages = _RecursiveLoader(_PageLoader(BasicPage, enja.load))
