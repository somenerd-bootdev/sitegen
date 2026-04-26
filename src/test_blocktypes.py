import unittest

from blocktypes import BlockType, block_to_block_type, markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type_heading(self):
        block_type = block_to_block_type("### Heading")
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_type_code(self):
        block_type = block_to_block_type("""
```
code
more code
bonus code
```
        """.strip())
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_type_quote(self):
        block_type = block_to_block_type("> Quote")
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_type_unordered_list(self):
        block_type = block_to_block_type("- One\n- Two\n- Three")
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_type_ordered_list(self):
        block_type = block_to_block_type("1. One\n2. Two\n3. Three")
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_type_paragraph(self):
        block_type = block_to_block_type("It's just text")
        self.assertEqual(block_type, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()