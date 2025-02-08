import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_mandatory_tag(self):
        self.assertRaises(TypeError, lambda _: ParentNode())

    def test_mandatory_children(self):
        self.assertRaises(TypeError, lambda _: ParentNode("p"))

    def test_none_tag(self):
        parent = ParentNode(None, [LeafNode("b", "text")])
        self.assertRaises(ValueError, parent.to_html)
    
    def test_none_children(self):
        parent = ParentNode("b", None)
        self.assertRaises(ValueError, parent.to_html)

    def test_repr(self):
        parent = ParentNode("p", [LeafNode("b", "text")], {"href": "https://www.google.com"})
        self.assertEqual(repr(parent), "ParentNode(p, [LeafNode(b, text, None)], {'href': 'https://www.google.com'})")

    def test_eq(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(parent.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()