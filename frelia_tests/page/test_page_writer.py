import frelia.page


def test_page_writer_missing_rendered_output(tmpdir, page):
    target_dir = str(tmpdir.join('dst'))
    writer = frelia.page.PageWriter(target_dir)
    assert page.rendered_output is None
    writer([page])
    assert not tmpdir.join('dst').check()


def test_page_writer(tmpdir, page):
    target_dir = str(tmpdir.join('dst'))
    writer = frelia.page.PageWriter(target_dir)
    page.rendered_output = 'rendered content'
    writer([page])
    rendered_file = tmpdir.join('dst/blog/page')
    assert rendered_file.read() == 'rendered content'
