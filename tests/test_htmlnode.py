import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        # Arrange
        tag = "div"
        value = "Hello World"
        children = [HTMLNode("p"), HTMLNode()]
        props = {
            "class": "bold",
            "style": "text-align: center",
        }

        # Act
        node = HTMLNode(tag, value, children, props)

        # Assert
        self.assertEqual(tag, node.tag)
        self.assertEqual(value, node.value)
        self.assertEqual(children, node.children)
        self.assertEqual(props, node.props)

    def test_init_none(self):
        # Act
        node = HTMLNode()

        # Assert
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual([], node.children)
        self.assertEqual({}, node.props)

    def test_props_to_html(self):
        # Arrange
        props = {
            "href": "https://test.example",
            "target": "_blank",
        }
        node = HTMLNode(props=props)

        expected = ' href="https://test.example" target="_blank"'

        # Act
        result = node.props_to_html()

        # Assert
        self.assertEqual(expected, result)

    def test_props_to_html_empty(self):
        # Arrange
        node = HTMLNode()

        # Act
        result = node.props_to_html()

        # Assert
        self.assertEqual('', result)

    def test_to_html_raises_not_implemented_error(self):
        # Arrange
        node = HTMLNode()

        # Act & Assert
        self.assertRaises(NotImplementedError, node.to_html)

    def test_repr(self):
        # Arrange
        tag = "div"
        value = "Hello World"
        children = [HTMLNode("p"), HTMLNode()]
        props = {
            "class": "bold",
            "style": "text-align: center",
        }

        node = HTMLNode(tag, value, children, props)

        expected = ("HTMLNode(tag='div', value='Hello World', "
                    "props={'class': 'bold', 'style': 'text-align: center'}, "
                    "children=['p', None])")

        # Act
        result = repr(node)

        # Assert
        self.assertEqual(expected, result)

    def test_repr_none(self):
        # Arrange
        node = HTMLNode()
        expected = "HTMLNode(tag=None, value=None, props={}, children=[])"

        # Act
        result = repr(node)

        # Assert
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
