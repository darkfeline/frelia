"""Document module.

This module defines the Document namedtuple.
"""

import collections

Document = collections.namedtuple('Document', 'header,body')
Document.__doc__ = """Document with metadata.

A document has two slots: header and body.  The header contains a metadata
dict, and the body contains a string.  The Document class does not dictate any
particular format for the header or the body.
"""
