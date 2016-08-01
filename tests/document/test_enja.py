import io
import textwrap

from frelia.document.formats import enja


def test_load():
    """Test parsing a simple enja document from a file."""
    text = textwrap.dedent("""\
    foo: bar
    ---
    <p>Hello world!</p>""")
    file = io.StringIO(text)
    doc = enja.load(file)
    assert doc.metadata == {'foo': 'bar'}
    assert doc.content == '<p>Hello world!</p>'


def test_dump(document):
    """Test parsing a simple enja document from a file."""
    file = io.StringIO()
    enja.dump(document, file)
    assert file.getvalue() == 'sophie: prachta\n---\ngirl meets girl'
