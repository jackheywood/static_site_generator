import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
