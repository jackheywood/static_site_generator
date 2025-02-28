import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_init(self):
        # Arrange
        tag = "div"
        children = [LeafNode("p", "Hello"), LeafNode("p", "World")]
        props = {
            "class": "bold",
            "style": "text-align: center",
        }

        # Act
        node = ParentNode(tag, children, props)

        # Assert
        self.assertEqual(tag, node.tag)
        self.assertEqual(children, node.children)
        self.assertEqual(props, node.props)
        self.assertIsNone(node.value)

    def test_to_html_no_tag(self):
        # Arrange
        node = ParentNode(None, [])

        # Act
        with self.assertRaises(ValueError) as error:
            node.to_html()

        # Assert
        self.assertEqual("ParentNode must have a tag", str(error.exception))

    def test_to_html_no_children(self):
        # Arrange
        node = ParentNode("div", None)

        # Act
        with self.assertRaises(ValueError) as error:
            node.to_html()

        # Assert
        self.assertEqual(
            "ParentNode must have at least one child node",
            str(error.exception),
        )

    def test_to_html_empty_children(self):
        # Arrange
        node = ParentNode("div", [])

        # Act
        with self.assertRaises(ValueError) as error:
            node.to_html()

        # Assert
        self.assertEqual(
            "ParentNode must have at least one child node",
            str(error.exception),
        )

    def test_to_html_single_child(self):
        # Arrange
        node = ParentNode("div", [LeafNode("p", "Hello")])

        # Act
        result = node.to_html()

        # Assert
        self.assertEqual("<div><p>Hello</p></div>", result)

    def test_to_html_multi_child(self):
        # Arrange
        node = ParentNode(
            "h1",
            [
                LeafNode("b", "Hello"),
                LeafNode("i", "World"),
                LeafNode(None, "!")
            ]
        )

        # Act
        result = node.to_html()

        # Assert
        self.assertEqual("<h1><b>Hello</b><i>World</i>!</h1>", result)

    def test_to_html_grandchildren(self):
        # Arrange
        node = ParentNode(
            "main",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("h1", "Hello"),
                    ]
                ),
                ParentNode(
                    "div",
                    [
                        LeafNode("h2", "World"),
                    ]
                )
            ]
        )

        # Act
        result = node.to_html()

        # Assert
        self.assertEqual(
            "<main><div><h1>Hello</h1></div><div><h2>World</h2></div></main>",
            result,
        )

    def test_to_html_props(self):
        # Arrange
        node = ParentNode(
            "div",
            [
                LeafNode("p", "Hi", {"class": "3", "id": "4"})
            ],
            {"class": "1", "id": "2"},
        )

        # Act
        result = node.to_html()

        # Assert
        self.assertEqual(
            '<div class="1" id="2"><p class="3" id="4">Hi</p></div>',
            result,
        )

    def test_repr(self):
        # Arrange
        tag = "div"
        children = [LeafNode("p", ""), LeafNode("i", "")]
        props = {
            "class": "bold",
            "style": "text-align: center",
        }

        node = ParentNode(tag, children, props)

        expected = ("ParentNode(tag='div', "
                    "props={'class': 'bold', 'style': 'text-align: center'}, "
                    "children=['p', 'i'])")

        # Act
        result = repr(node)

        # Assert
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
