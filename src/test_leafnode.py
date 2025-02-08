import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")

    def test_eq_attr(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_eq_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_mandatory_tag(self):
        self.assertRaises(TypeError, lambda _: LeafNode())

    def test_mandatory_value(self):
        self.assertRaises(TypeError, lambda : LeafNode("p"))

    def test_value_not_none(self):
        leaf = LeafNode("p", None)
        self.assertRaises(ValueError, leaf.to_html)
    
    def test_repr(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(leaf), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")

if __name__ == "__main__":
    unittest.main()