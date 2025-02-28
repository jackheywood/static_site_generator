from block_markdown import BlockType
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def paragraph_to_html_node(block):
    paragraph = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode("p", text_to_children(paragraph))


def heading_to_html_node(block):
    hashes, text = block.split(" ", 1)
    heading_level = len(hashes)
    return ParentNode(f"h{heading_level}", text_to_children(text))


def code_to_html_node(block):
    code = block.split("\n", 1)[1].rstrip("```")  # Ignore language
    code_text_node = TextNode(code, TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(code_text_node)])


def quote_to_html_node(block):
    quote_lines = [line.lstrip(">").strip() for line in block.split("\n")]
    text = " ".join(quote_lines)
    return ParentNode("blockquote", text_to_children(text))


def ulist_block_to_html_node(block):
    return list_block_to_html_node(block, "ul")


def olist_block_to_html_node(block):
    return list_block_to_html_node(block, "ol")


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
    text_nodes = text_to_textnodes(text)
    return [
        text_node_to_html_node(node)
        for node in text_nodes
    ]


BLOCK_HANDLERS = {
    BlockType.PARAGRAPH: paragraph_to_html_node,
    BlockType.HEADING: heading_to_html_node,
    BlockType.CODE: code_to_html_node,
    BlockType.QUOTE: quote_to_html_node,
    BlockType.ULIST: ulist_block_to_html_node,
    BlockType.OLIST: olist_block_to_html_node
}
