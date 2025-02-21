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
            extract_and_split_node(
                node,
                extract_markdown_images,
                TextType.IMAGE,
            )
        )

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        new_nodes.extend(
            extract_and_split_node(
                node,
                extract_markdown_links,
                TextType.LINK,
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


def extract_and_split_node(
        node,
        markdown_extractor,
        extracted_type):
    if node.text_type != TextType.TEXT:
        return [node]

    new_nodes = []
    extracted_matches = markdown_extractor(node.text)

    start = 0
    for ((text, url), match_start, match_end) in extracted_matches:
        if start < match_start:
            text_node = TextNode(node.text[start:match_start], TextType.TEXT)
            new_nodes.append(text_node)

        extracted_node = TextNode(text, extracted_type, url)
        new_nodes.append(extracted_node)
        start = match_end

    if start < len(node.text):
        final_node = TextNode(node.text[start:], TextType.TEXT)
        new_nodes.append(final_node)

    return new_nodes


def extract_markdown_images(text):
    return extract_markdown_with_positions(
        r"!\[([^\[\]]*)]\(([^()]*)\)",
        text,
    )


def extract_markdown_links(text):
    return extract_markdown_with_positions(
        r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)",
        text,
    )


def extract_markdown_with_positions(regex, text):
    matches = re.finditer(regex, text)
    return [
        (match.groups(), match.start(), match.end())
        for match in matches
    ]
