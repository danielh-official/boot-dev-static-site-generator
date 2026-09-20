import unittest
from leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is not a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode(None, TextType.LINK)
        self.assertIsNone(node.url)

    def test_text_node_to_html_node(self):
        cases = [
            (TextNode("t", TextType.PLAIN), LeafNode(None, "t")),
            (TextNode("t", TextType.BOLD), LeafNode("b", "t")),
            (TextNode("t", TextType.ITALIC), LeafNode("i", "t")),
            (TextNode("t", TextType.CODE), LeafNode("code", "t")),
            (TextNode("t", TextType.LINK, "http://x"), LeafNode("a", "t", {"href": "http://x"})),
            (TextNode("t", TextType.IMAGE, "http://x"), LeafNode("img", "", {"src": "http://x", "alt": "t"})),
        ]
        for text_node, expected in cases:
            self.assertEqual(repr(text_node.text_node_to_html_node(text_node)), repr(expected))

    def test_text_node_to_html_node_unknown_type(self):
        with self.assertRaises(ValueError):
            bad = TextNode("t", "nope")  # type: ignore[arg-type]  # deliberately invalid
            bad.text_node_to_html_node(bad)


if __name__ == "__main__":
    unittest.main()