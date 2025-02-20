import unittest
from parsing import split_nodes_delimiter
from textnode import TextNode, TextType


class TestParsing(unittest.TestCase):
    def test_split_nodes_delimiter_single_node(self):
        # Arrange
        node = TextNode("Text with **bold phrase** inside", TextType.TEXT)

        # Act
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Assert
        self.assertEqual(3, len(result))
        self.assertEqual(TextNode("Text with ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("bold phrase", TextType.BOLD), result[1])
        self.assertEqual(TextNode(" inside", TextType.TEXT), result[2])

    def test_split_nodes_delimiter_end_of_text(self):
        # Arrange
        node = TextNode("Text with code `at the end`", TextType.TEXT)

        # Act
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # Assert
        self.assertEqual(2, len(result))
        self.assertEqual(TextNode("Text with code ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("at the end", TextType.CODE), result[1])

    def test_split_nodes_delimiter_start_of_text(self):
        # Arrange
        node = TextNode("*Italic text* at the start", TextType.TEXT)

        # Act
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)

        # Assert
        self.assertEqual(2, len(result))
        self.assertEqual(TextNode("Italic text", TextType.ITALIC), result[0])
        self.assertEqual(TextNode(" at the start", TextType.TEXT), result[1])

    def test_split_nodes_no_closing_delimiter(self):
        # Arrange
        node = TextNode("Text without **closing delimiter", TextType.TEXT)

        # Act
        with self.assertRaises(ValueError) as error:
            split_nodes_delimiter([node], "**", TextType.BOLD)

        # Assert
        self.assertEqual(
            "No closing '**' delimiter found in input text",
            str(error.exception)
        )

    def test_split_nodes_not_text_node(self):
        # Arrange
        node = TextNode("Already **a** link", TextType.LINK)

        # Act
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Assert
        self.assertEqual([node], result)

    def test_split_nodes_multiple_delimiters(self):
        # Arrange
        node = TextNode("`code` with `code` and `more code`!", TextType.TEXT)

        # Act
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # Assert
        self.assertEqual(6, len(result))
        self.assertEqual(TextNode("code", TextType.CODE), result[0])
        self.assertEqual(TextNode(" with ", TextType.TEXT), result[1])
        self.assertEqual(TextNode("code", TextType.CODE), result[2])
        self.assertEqual(TextNode(" and ", TextType.TEXT), result[3])
        self.assertEqual(TextNode("more code", TextType.CODE), result[4])
        self.assertEqual(TextNode("!", TextType.TEXT), result[5])

    def test_split_nodes_multiple_nodes(self):
        # Arrange
        node1 = TextNode("Text with **bold** section", TextType.TEXT)
        node2 = TextNode("Text with *italic*", TextType.TEXT)
        node3 = TextNode("Image", TextType.IMAGE)
        node4 = TextNode("More **bold text**", TextType.TEXT)
        node5 = TextNode("Code", TextType.CODE)

        # Act
        result = split_nodes_delimiter(
            [node1, node2, node3, node4, node5],
            "**",
            TextType.BOLD
        )

        # Assert
        self.assertEqual(8, len(result))
        self.assertEqual(TextNode("Text with ", TextType.TEXT), result[0])
        self.assertEqual(TextNode("bold", TextType.BOLD), result[1])
        self.assertEqual(TextNode(" section", TextType.TEXT), result[2])
        self.assertEqual(node2, result[3])
        self.assertEqual(node3, result[4])
        self.assertEqual(TextNode("More ", TextType.TEXT), result[5])
        self.assertEqual(TextNode("bold text", TextType.BOLD), result[6])
        self.assertEqual(node5, result[7])
