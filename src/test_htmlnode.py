import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_without_tag_returns_raw_text(self):
        node = HTMLNode(value="Hello, world!")

        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_value(self):
        node = HTMLNode(tag="p", value="Hello, world!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        node = HTMLNode(
            tag="div",
            children=[
                HTMLNode(tag="p", value="First"),
                HTMLNode(tag="p", value="Second"),
            ],
        )

        self.assertEqual(node.to_html(), "<div><p>First</p><p>Second</p></div>")

    def test_to_html_with_props(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Google</a>',
        )

    def test_to_html_without_props(self):
        node = HTMLNode(tag="p", value="No attributes")

        self.assertEqual(node.to_html(), "<p>No attributes</p>")

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_without_props(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
