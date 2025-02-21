import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, delimited_type):
    new_nodes = []

    for node in old_nodes:
        new_nodes.extend(split_node_delimiter(node, delimiter, delimited_type))

    return new_nodes


def split_node_delimiter(node, delimiter, delimited_type):
    if node.text_type != TextType.TEXT:
        return [node]

    sections = node.text.split(delimiter)

    if len(sections) % 2 == 0:
        raise ValueError(
            f"No closing '{delimiter}' delimiter found in input text: "
            f'"{node.text}"'
        )

    return [
        TextNode(text, delimited_type if i % 2 != 0 else TextType.TEXT)
        for i, text in enumerate(sections) if text
    ]


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)
