import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        # Arrange
        tag = "div"
        value = "Hello World"
        props = {
            "class": "bold",
            "style": "text-align: center",
        }

        # Act
        node = LeafNode(tag, value, props)

        # Assert
        self.assertEqual(tag, node.tag)
        self.assertEqual(value, node.value)
        self.assertEqual(props, node.props)
        self.assertEqual([], node.children)

    def test_to_html_no_value(self):
        # Arrange
        node = LeafNode("p", None)

        # Act & Assert
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        # Arrange
        value = "Hello World"
        node = LeafNode(None, value)

        # Act
        result = node.to_html()

        # Assert
        self.assertEqual(value, result)

    def test_to_html(self):
        # Arrange
        tag = "a"
        value = "Hello world!"
        props = {"class": "bold", "id": "1"}
        node = LeafNode(tag, value, props)

        # Act
        result = node.to_html()

        # Assert
        self.assertEqual(f'<{tag} class="bold" id="1">{value}</{tag}>', result)

    def test_repr(self):
        # Arrange
        tag = "div"
        value = "Hello World"
        props = {
            "class": "bold",
            "style": "text-align: center",
        }

        node = LeafNode(tag, value, props)

        expected = ("LeafNode(tag='div', value='Hello World', "
                    "props={'class': 'bold', 'style': 'text-align: center'})")

        # Act
        result = repr(node)

        # Assert
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
