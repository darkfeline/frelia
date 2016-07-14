import datetime

import pytest

from frelia import sitemap


def test_url_only_loc():
    sitemap.URL('http://localhost/')


def test_url():
    sitemap.URL(
        loc='http://localhost/',
        lastmod=datetime.datetime(2010, 1, 2),
        changefreq='daily',
        priority=0.5)


def test_url_invalid_lastmod():
    with pytest.raises(sitemap.ValidationError):
        sitemap.URL(
            loc='http://localhost/',
            lastmod=datetime.time(1, 2, 3))


def test_url_invalid_changefreq():
    with pytest.raises(sitemap.ValidationError):
        sitemap.URL(
            loc='http://localhost/',
            changefreq='DAILY')


def test_url_invalid_priority():
    with pytest.raises(sitemap.ValidationError):
        sitemap.URL(
            loc='http://localhost/',
            priority=1.1)
