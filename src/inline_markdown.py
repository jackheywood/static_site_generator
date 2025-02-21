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
        new_nodes.extend(
            split_node_with_extractor(
                node,
                extract_markdown_images,
                split_markdown_image,
                TextType.IMAGE
            )
        )

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        new_nodes.extend(
            split_node_with_extractor(
                node,
                extract_markdown_links,
                split_markdown_link,
                TextType.LINK
            )
        )

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


def split_node_with_extractor(node, extractor, splitter, extracted_type):
    if node.text_type != TextType.TEXT:
        return [node]

    new_nodes = []
    extracted = extractor(node.text)
    remaining_markdown = node.text

    for (text, url) in extracted:
        sections = splitter(remaining_markdown, text, url)
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(text, extracted_type, url))
        remaining_markdown = sections[1]

    if remaining_markdown:
        new_nodes.append(TextNode(remaining_markdown, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)


def split_markdown_image(markdown, alt, url):
    return markdown.split(f"![{alt}]({url})", 1)


def split_markdown_link(markdown, text, url):
    return markdown.split(f"[{text}]({url})", 1)
