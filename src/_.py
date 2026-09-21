import re
from enum import Enum

from textnode import TextNode, TextType


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


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


def _split_nodes_markdown(
    old_nodes: list[TextNode], extractor, markdown_type: TextType, prefix: str
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text is None or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extractor(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        remaining = node.text
        while True:
            match = matches[0]
            label, url = match
            markdown = f"{prefix}[{label}]({url})" if prefix else f"[{label}]({url})"
            parts = remaining.split(markdown, 1)
            if len(parts) == 1:
                break

            before, remaining = parts
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(label, markdown_type, url))
            matches = extractor(remaining)
            if not matches:
                if remaining:
                    new_nodes.append(TextNode(remaining, TextType.TEXT))
                break

        if not matches and not remaining:
            continue

    return [node for node in new_nodes if node.text]


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_markdown(
        old_nodes, extract_markdown_images, TextType.IMAGE, "!"
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_markdown(old_nodes, extract_markdown_links, TextType.LINK, "")


def markdown_to_blocks(markdown: str) -> list[str]:
    if markdown is None:
        return []

    markdown = markdown.strip()
    if not markdown:
        return []

    blocks = re.split(r"\n\s*\n+", markdown)
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    if re.fullmatch(r"```\n[\s\S]*\n```", block):
        return BlockType.CODE

    lines = block.splitlines()
    if lines and all(re.match(r"> ?.*", line) for line in lines):
        return BlockType.QUOTE

    if lines and all(re.match(r"- .+", line) for line in lines):
        return BlockType.UNORDERED_LIST

    if lines:
        ordered_list_pattern = re.compile(r"^(\d+)\. .+")
        if all(ordered_list_pattern.match(line) for line in lines):
            numbers = [
                int(match.group(1))
                for line in lines
                for match in [ordered_list_pattern.match(line)]
                if match
            ]
            if numbers == list(range(1, len(numbers) + 1)):
                return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
