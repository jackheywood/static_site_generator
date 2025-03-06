from block_handlers import BLOCK_HANDLERS
from block_markdown import markdown_to_blocks, block_to_block_type
from parentnode import ParentNode


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [
        block_to_html_node(block)
        for block in blocks
    ]
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    handler = BLOCK_HANDLERS.get(block_type)
    if not handler:
        raise ValueError(f"No handler for block type: {block_type}")
    return handler(block)


def extract_title(markdown):
    lines = [line.strip() for line in markdown.split("\n")]
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"No title found for markdown")
