from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode


def main():
    node = TextNode('Hello World', TextType.ITALIC, "https://example.com")
    print(node)

    parent = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text"),
        ]
    )

    print(parent.to_html())


if __name__ == '__main__':
    main()
