"""Sitemaps.

http://www.sitemaps.org/protocol.html

"""

import datetime
import numbers

import frelia.jinja


class URL:

    """Represents a sitemap url."""

    def __init__(self, loc, lastmod=None, changefreq=None, priority=None):
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority
        self.validate()

    def validate(self):
        self._validate_lastmod()
        self._validate_changefreq()
        self._validate_priority()

    def _validate_lastmod(self):
        bad = (
            self.lastmod is not None
            and not isinstance(self.lastmod, datetime.date))
        if bad:
            raise ValidationError('lastmod must be a date or datetime.')

    _VALID_CHANGEFREQ = [
        'always',
        'hourly',
        'daily',
        'weekly',
        'monthly',
        'yearly',
        'never',
    ]

    def _validate_changefreq(self):
        bad = (
            self.changefreq is not None
            and self.changefreq not in self._VALID_CHANGEFREQ)
        if bad:
            raise ValidationError('changefreq must be one of a few valid values.')

    def _validate_priority(self):
        bad = (
            self.priority is not None
            and not (
                isinstance(self.priority, numbers.Real)
                and 0 <= self.priority <= 1))
        if bad:
            raise ValidationError('priority must be a float between 0.0 and 1.0.')


def render(urls):
    """Render sitemap.xml content using provided URLs.

    urls is an iterable.

    """
    context = {'urls': urls}
    env = frelia.jinja.Environment()
    template = env.get_template('sitemap.xml')
    return template.render(context)


class ValidationError(Exception): pass
