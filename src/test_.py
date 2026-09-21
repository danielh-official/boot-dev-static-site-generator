import unittest

from _ import split_nodes_delimiter
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


if __name__ == "__main__":
    unittest.main()
