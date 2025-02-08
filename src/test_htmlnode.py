import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_wrong_children(self):
        self.assertRaises(TypeError, lambda _: HTMLNode(children="not working"))

    def test_wrong_props(self):
        self.assertRaises(TypeError, lambda _: HTMLNode(props="not working"))

    def test_to_html(self):
        html = HTMLNode()
        self.assertRaises(NotImplementedError, html.to_html)

    def test_empty_repr(self):
        html = HTMLNode()
        self.assertEqual(repr(html), "HTMLNode(None, None, None, None)")

    def test_non_empty_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

    def test_props_to_html(self):
        html = HTMLNode(props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(html.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_equal_props(self):
        html1 = HTMLNode(value="test1", props={"href":"https://www.google.com", "target":"_blank"})
        html2 = HTMLNode(value="test2", props={"href":"https://www.google.com", "target":"_blank"})

        self.assertEqual(html1.props_to_html(), html2.props_to_html())

    def test_diff_props(self):
        html1 = HTMLNode(value="test1", props={"href":"https://www.google.com", "target":"_blank", "data": "none"})
        html2 = HTMLNode(value="test2", props={"href":"https://www.google.com", "target":"_blank"})

        self.assertNotEqual(html1.props_to_html(), html2.props_to_html())
