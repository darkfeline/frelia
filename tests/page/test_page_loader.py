import mir.frelia.page as page_mod


def test_load_pages(tmpdir, simple_document_reader):
    root = tmpdir.mkdir('root')
    filepath = root.mkdir('blog').join('post')
    filepath.write('test')
    loader = page_mod.PageLoader(simple_document_reader)

    got = list(loader(str(root)))

    assert len(got) == 1
    page = got[0]
    assert page.path == str(filepath)
    assert page.document.body == 'test'
