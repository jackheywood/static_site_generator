import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, delimited_type):
    new_nodes = []

    for node in old_nodes:
        new_nodes.extend(split_node_delimiter(node, delimiter, delimited_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        new_nodes.extend(split_node_image(node))

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


def split_node_image(node):
    if node.text_type != TextType.TEXT:
        return [node]

    new_nodes = []
    images = extract_markdown_images(node.text)
    text = node.text

    for (image_alt, image_url) in images:
        sections = text.split(f"![{image_alt}]({image_url})", 1)
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
        text = sections[1]

    if text:
        new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)
