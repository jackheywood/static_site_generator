from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(block_to_html_node(block))
    return ParentNode("div", nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block))
        case BlockType.HEADING:
            hashes, text = block.split(" ", 1)
            return ParentNode(f"h{len(hashes)}", text_to_children(text))
        case BlockType.CODE:
            code = block.split("\n", 1)[1].rstrip("```")  # Ignore language
            code_text_node = TextNode(code, TextType.CODE)
            return ParentNode("pre", [text_node_to_html_node(code_text_node)])
        case BlockType.QUOTE:
            quote = block.replace(">", "")
            return ParentNode("blockquote", text_to_children(quote))
        case BlockType.ULIST:
            return list_block_to_html_node(block, "ul")
        case BlockType.OLIST:
            return list_block_to_html_node(block, "ol")
        case _:
            raise ValueError(f"Invalid block type: {block_type}")


def list_block_to_html_node(block, list_tag):
    list_items = [
        line.split(" ", 1)[1]
        for line in block.split("\n")
    ]
    list_nodes = [
        ParentNode("li", text_to_children(item))
        for item in list_items
    ]
    return ParentNode(list_tag, list_nodes)


def text_to_children(text):
    single_line_text = " ".join(text.split())
    text_nodes = text_to_textnodes(single_line_text)
    return [
        text_node_to_html_node(node)
        for node in text_nodes
    ]
