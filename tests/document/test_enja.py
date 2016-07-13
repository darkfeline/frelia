import io
import textwrap

from frelia.document import base
from frelia.document import enja


def test_read():
    """Test parsing a simple enja document from a file."""
    text = textwrap.dedent("""\
    foo: bar
    ---
    <p>Hello world!</p>""")
    file = io.StringIO(text)
    doc = enja.read(file)
    assert doc.metadata == {'foo': 'bar'}
    assert doc.content == '<p>Hello world!</p>'


def test_write():
    """Test parsing a simple enja document from a file."""
    file = io.StringIO()
    document = base.Document({'foo': 'bar'}, '<p>Hello world!</p>')
    enja.write(document, file)
    assert file.getvalue() == 'foo: bar\n---\n<p>Hello world!</p>'
