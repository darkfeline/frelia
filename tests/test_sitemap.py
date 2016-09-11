import datetime
import io

import pytest

from mir.frelia import sitemap


@pytest.mark.parametrize(
    ('loc', 'lastmod', 'changefreq', 'priority'),
    [
        ('http://localhost/', None, None, None),
        ('http://localhost/', datetime.datetime(2010, 1, 2), 'daily', 0.5),
    ])
def test_valid_url(loc, lastmod, changefreq, priority):
    """Test constructing valid URLs."""
    url = sitemap.URL(
        loc=loc,
        lastmod=lastmod,
        changefreq=changefreq,
        priority=priority)
    assert url.loc == loc
    assert url.lastmod == lastmod
    assert url.changefreq == changefreq
    assert url.priority == priority


@pytest.mark.parametrize(
    ('loc', 'lastmod', 'changefreq', 'priority'),
    [
        ('http://localhost/', datetime.time(1, 2, 3), None, None),
        ('http://localhost/', None, 'DAILY', None),
        ('http://localhost/', None, None, 1.1),
    ])
def test_invalid_urls(loc, lastmod, changefreq, priority):
    """Test constructing invalid URLs."""
    with pytest.raises(sitemap.ValidationError):
        sitemap.URL(
            loc=loc,
            lastmod=lastmod,
            changefreq=changefreq,
            priority=priority)


def test_render():
    """Test rendering a sitemap urlset."""
    url = sitemap.URL(
        loc='http://localhost/',
        lastmod=datetime.date(2010, 1, 2),
        changefreq='daily',
        priority=0.7)
    file = io.StringIO()
    sitemap.render(file, [url])
    assert file.getvalue() == (
        "<?xml version='1.0' encoding='UTF-8'?>\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9'
        ' http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
        '<url><loc>http://localhost/</loc><lastmod>2010-01-02</lastmod>'
        '<changefreq>daily</changefreq><priority>0.7</priority></url>'
        '</urlset>')
