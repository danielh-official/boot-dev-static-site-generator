import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text is None or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax: missing closing delimiter '{delimiter}' in text {node.text!r}"
            )

        split_parts: list[TextNode] = []
        for i, part in enumerate(parts):
            if part == "" and (i == 0 or i == len(parts) - 1):
                continue
            if i % 2 == 0:
                if part:
                    split_parts.append(TextNode(text=part, text_type=TextType.TEXT))
            else:
                if part:
                    split_parts.append(TextNode(text=part, text_type=text_type))

        new_nodes.extend(split_parts)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)