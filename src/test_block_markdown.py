import unittest

from block_markdown import markdown_to_blocks, block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_paragraph(self):
        text = """this is a paragraph
absolute classic!"""
        self.assertEqual(block_to_block_type(text), "paragraph")
    
    def test_heading(self):
        h1 = "# header1"
        h2 = "## header2"
        h3 = "### header3"
        h4 = "#### header4"
        h5 = "##### header5"
        h6 = "###### header6"
        fake_h = "#@ non header"

        self.assertEqual(block_to_block_type(h1), "heading")
        self.assertEqual(block_to_block_type(h2), "heading")
        self.assertEqual(block_to_block_type(h3), "heading")
        self.assertEqual(block_to_block_type(h4), "heading")
        self.assertEqual(block_to_block_type(h5), "heading")
        self.assertEqual(block_to_block_type(h6), "heading")
        self.assertEqual(block_to_block_type(fake_h), "paragraph")

    def test_code(self):
        code = """```python
testing some code here
```"""
        fake_code = """``
should not work
``"""
        self.assertEqual(block_to_block_type(code), "code")
        self.assertEqual(block_to_block_type(fake_code), "paragraph")

    def test_quote(self):
        quote = """>One quote
> Two quote"""
        not_quote = """> One quote
two quote"""

        self.assertEqual(block_to_block_type(quote), "quote")
        self.assertEqual(block_to_block_type(not_quote), "paragraph")
    
    def test_unordered_list(self):
        unordered = """* One
- Two"""
        fake = """*Nope
- No"""
        fake_two = """@ No
Won't do"""
        fake_three = """* Yes
No"""
        self.assertEqual(block_to_block_type(unordered), "unordered_list")
        self.assertEqual(block_to_block_type(fake), "paragraph")
        self.assertEqual(block_to_block_type(fake_two), "paragraph")
        self.assertEqual(block_to_block_type(fake_three), "paragraph")

    def test_ordered_list(self):
        ordered = """1. One
2. Two"""
        fake = """2. One
1. Two"""
        self.assertEqual(block_to_block_type(ordered), "ordered_list")
        self.assertEqual(block_to_block_type(fake), "paragraph")


if __name__ == "__main__":
    unittest.main()