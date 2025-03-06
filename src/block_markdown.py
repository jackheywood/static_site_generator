import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n") if block]


def block_to_block_type(block):
    if not block or not isinstance(block, str):
        raise ValueError("Input must be a non-empty string")

    # Code block: Fenced code syntax using backticks
    # Closing backticks must be on a new line
    if re.search(r"^```", block) and re.search(r"\n```$", block):
        return BlockType.CODE

    # Heading: Lines starting with # (1-6)
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING

    lines = block.split("\n")

    # Quote: All lines start with ">"
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: All lines must start with the same consistent marker
    # ("- " or "* ")
    if all(line.startswith("* ") for line in lines):
        return BlockType.ULIST
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST

    # Ordered list: All lines start with "N. " where N is a digit starting at 1
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.OLIST

    # Default to paragraph
    return BlockType.PARAGRAPH
