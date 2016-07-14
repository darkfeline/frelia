import datetime

import pytest

from frelia import sitemap


@pytest.fixture
def url():
    return sitemap.URL(
        loc='http://localhost/',
        lastmod=datetime.date(2010, 1, 2),
        changefreq='daily',
        priority=0.7)


def test_render_empty():
    got = sitemap.render(())
    assert got == """\
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
</urlset>"""


def test_render(url):
    got = sitemap.render([url])
    assert got == """\
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  <url>
    <loc>http://localhost/</loc>
    <lastmod>2010-01-02</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>"""
