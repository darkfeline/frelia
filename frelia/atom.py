"""Atom feeds.

https://tools.ietf.org/html/rfc4287

"""

import frelia.jinja


def render(feed):
    context = {'feed': feed}
    env = frelia.jinja.Environment()
    template = env.get_template('atom.xml')
    return template.render(context)


class Feed:

    def __init__(
            self,
            id,
            title,
            updated,
            rights=None,
            links=(),
            authors=(),
            entries=()):
        self.id = id
        self.title = title
        self.updated = updated
        self.rights = rights
        self.links = links
        self.authors = authors
        self.entries = entries


class Author:

    def __init__(self, name, uri=None, email=None):
        self.name = name
        self.uri = uri
        self.email = email


class Entry:

    def __init__(
            self,
            id,
            title,
            updated,
            summary=None,
            published=None,
            links=(),
            categories=()):
        self.id = id
        self.title = title
        self.updated = updated
        self.summary = summary
        self.published = published
        self.links = links
        self.categories = categories


class Link:

    def __init__(self, href, rel=None, type=None):
        self.href = href
        self.rel = rel
        self.type = type


class Category:

    def __init__(self, term, scheme=None, label=None):
        self.term = term
        self.scheme = scheme
        self.label = label
