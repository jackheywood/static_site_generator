import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Arrange
        text = "This is a test"
        text_type = TextType.BOLD

        node1 = TextNode(text, text_type)
        node2 = TextNode(text, text_type)

        # Assert
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        # Arrange
        text = "This is a test"
        text_type = TextType.BOLD
        url = "https://test.com"

        node1 = TextNode(text, text_type, url)
        node2 = TextNode(text, text_type, url)

        # Assert
        self.assertEqual(node1, node2)

    def test_different_text_not_eq(self):
        # Arrange
        text_type = TextType.BOLD

        node1 = TextNode("Text 1", text_type)
        node2 = TextNode("Text 2", text_type)

        # Assert
        self.assertNotEqual(node1, node2)

    def test_different_text_type_not_eq(self):
        # Arrange
        text = "This is a test"

        node1 = TextNode(text, TextType.LINK)
        node2 = TextNode(text, TextType.NORMAL)

        # Assert
        self.assertNotEqual(node1, node2)

    def test_different_url_not_eq(self):
        # Arrange
        text = "This is a test"
        text_type = TextType.BOLD

        node1 = TextNode(text, text_type, "https://test.co.uk")
        node2 = TextNode(text, text_type, "https://test.com")

        # Assert
        self.assertNotEqual(node1, node2)

    def test_init(self):
        # Arrange
        text = "Testing"
        text_type = TextType.CODE
        url = "https://test.example"

        # Act
        node = TextNode(text, text_type, url)

        # Assert
        self.assertEqual(text, node.text)
        self.assertEqual(text_type, node.text_type)
        self.assertEqual(url, node.url)

    def test_repr(self):
        # Arrange
        text = "Testing"
        text_type = TextType.LINK
        url = "https://test.example"
        node = TextNode(text, text_type, url)
        expected_repr = f"TextNode({text}, {text_type.value}, {url})"

        # Act
        result = repr(node)

        # Assert
        self.assertEqual(expected_repr, result)

    def test_none_eq(self):
        # Arrange
        node1 = TextNode(None, None, None)
        node2 = TextNode(None, None, None)

        # Assert
        self.assertEqual(node1, node2)

    def test_none_init(self):
        # Act
        node = TextNode(None, None, None)

        # Assert
        self.assertIsNone(node.text)
        self.assertIsNone(node.text_type)
        self.assertIsNone(node.url)

    def test_none_repr(self):
        # Arrange
        node = TextNode(None, None, None)
        expected_repr = f"TextNode(None, None, None)"

        # Act
        result = repr(node)

        # Assert
        self.assertEqual(expected_repr, result)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_normal_text_node_to_html_node(self):
        # Arrange
        text = "Text"
        node = TextNode(text, TextType.NORMAL)

        # Act
        result = text_node_to_html_node(node)

        # Assert
        self.assertEqual(text, result.to_html())

    def test_bold_text_node_to_html_node(self):
        # Arrange
        text = "Woah!"
        node = TextNode(text, TextType.BOLD)

        # Act
        result = text_node_to_html_node(node)

        # Assert
        self.assertEqual(f"<b>{text}</b>", result.to_html())

    def test_italic_text_node_to_html_node(self):
        # Arrange
        text = "Zip zoom"
        node = TextNode(text, TextType.ITALIC)

        # Act
        result = text_node_to_html_node(node)

        # Assert
        self.assertEqual(f"<i>{text}</i>", result.to_html())

    def test_code_text_node_to_html_node(self):
        # Arrange
        text = "[x for x in range(23)]"
        node = TextNode(text, TextType.CODE)

        # Act
        result = text_node_to_html_node(node)

        # Assert
        self.assertEqual(f"<code>{text}</code>", result.to_html())

    def test_link_text_node_to_html_node(self):
        # Arrange
        text = "Example Link"
        url = "https://test.example"
        node = TextNode(text, TextType.LINK, url)

        # Act
        result = text_node_to_html_node(node)

        # Assert
        self.assertEqual(f'<a href="{url}">{text}</a>', result.to_html())

    def test_image_text_node_to_html_node(self):
        # Arrange
        text = "A dog"
        url = "https://test.example/dog.jpeg"
        node = TextNode(text, TextType.IMAGE, url)

        # Act
        result = text_node_to_html_node(node)

        # Assert
        self.assertEqual(
            f'<img src="{url}" alt="{text}"></img>',
            result.to_html(),
        )

    def test_invalid_text_node_to_html_node(self):
        # Arrange
        text_type = "UNKNOWN"
        node = TextNode("", text_type)

        # Act
        with self.assertRaises(ValueError) as error:
            text_node_to_html_node(node)

        # Assert
        self.assertEqual(
            f"Invalid text type: {text_type}",
            str(error.exception),
        )


if __name__ == "__main__":
    unittest.main()
