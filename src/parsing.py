from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError(
                    f"No closing '{delimiter}' delimiter found in input text"
                )
            for i in range(len(split_text)):
                if i % 2 != 0:
                    new_nodes.append(TextNode(split_text[i], text_type))
                elif split_text[i] != "":
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))

    return new_nodes
