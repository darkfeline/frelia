import pytest

import mir.frelia.page as page_mod


@pytest.mark.parametrize('pages', [
    [
        page_mod.Page('blog/page', 'rendered content'),
    ]
])
def test_page_writer(tmpdir, pages):
    target_dir = str(tmpdir.join('dst'))
    writer = page_mod.PageWriter(target_dir)
    writer(pages)
    rendered_file = tmpdir.join('dst/blog/page')
    assert rendered_file.read() == 'rendered content'
