import unittest

from _ import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_keeps_text_around_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_split_nodes_delimiter_with_bold_phrase(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_split_nodes_delimiter_ignores_non_text_nodes(self):
        node = TextNode("This is bold", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [node])

    def test_split_nodes_delimiter_raises_on_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, "missing closing delimiter"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)
        
    def test_extract_markdown_links(self):
        text = "This is text with a [Google](https://www.google.com) and [OpenAI](https://www.openai.com)"
        expected = [
            ("Google", "https://www.google.com"),
            ("OpenAI", "https://www.openai.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_split_nodes_image(self):
        nodes = [
            TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and more", TextType.TEXT)
        ]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and more", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_link(self):
        nodes = [
            TextNode("This is text with a [Google](https://www.google.com) and more", TextType.TEXT)
        ]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" and more", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_image_no_match_returns_original_node(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_split_nodes_link_no_match_returns_original_node(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

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


if __name__ == "__main__":
    unittest.main()
