import unittest

from markdown import markdown_to_html_node, extract_title


class TestMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        # Arrange
        md = """
This is **bolded** paragraph
 text in a p
tag here

This one has _italic_ text and `code`

![image](https://image.example/img.png)

"""
        # Act
        node = markdown_to_html_node(md)

        # Assert
        self.assertEqual(
            "<div>"
            "<p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This one has <i>italic</i> text and <code>code</code></p>"
            '<p><img src="https://image.example/img.png" alt="image"></img></p>'
            "</div>",
            node.to_html()
        )

    def test_code_block(self):
        # Arrange
        md = """
```py
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        # Act
        node = markdown_to_html_node(md)

        # Assert
        self.assertEqual(
            "<div>"
            "<pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n</code></pre>"
            "</div>",
            node.to_html(),
        )

    def test_headings(self):
        # Arrange
        md = """
# This is a **bold heading**

### This is a subheading with `code`

###### This is a [link](https://www.google.com)

"""

        # Act
        node = markdown_to_html_node(md)

        # Assert
        self.assertEqual(
            "<div>"
            "<h1>This is a <b>bold heading</b></h1>"
            "<h3>This is a subheading with <code>code</code></h3>"
            "<h6>This is a <a href=\"https://www.google.com\">link</a></h6>"
            "</div>",
            node.to_html(),
        )

    def test_quote(self):
        # Arrange
        md = """
> This is a **quote**
>with inconsistent _spacing_
"""
        # Act
        node = markdown_to_html_node(md)

        # Assert
        self.assertEqual(
            "<div>"
            "<blockquote>"
            "This is a <b>quote</b> with inconsistent <i>spacing</i>"
            "</blockquote>"
            "</div>",
            node.to_html(), )

    def test_unordered_lists(self):
        # Arrange
        md = """
- This is a **list item**
- For a list using -

* This is *another* list item
* With a different delimiter
"""

        # Act
        node = markdown_to_html_node(md)

        # Assert
        self.assertEqual(
            "<div>"
            "<ul>"
            "<li>This is a <b>list item</b></li>"
            "<li>For a list using -</li>"
            "</ul>"
            "<ul>"
            "<li>This is <i>another</i> list item</li>"
            "<li>With a different delimiter</li>"
            "</ul>"
            "</div>",
            node.to_html()
        )

    def test_ordered_list(self):
        # Arrange
        md = """
1. This is a **list item**
2. In an order
3. With a [link](https://www.google.com)
4. And ![image](https://image.example)
"""

        # Act
        node = markdown_to_html_node(md)

        # Assert
        self.assertEqual(
            "<div>"
            "<ol>"
            "<li>This is a <b>list item</b></li>"
            "<li>In an order</li>"
            '<li>With a <a href="https://www.google.com">link</a></li>'
            '<li>And <img src="https://image.example" alt="image"></img></li>'
            "</ol>"
            "</div>",
            node.to_html()
        )

    def test_extract_title(self):
        # Arrange
        md = """
This is markdown
## With an h2
#   And a title 
"""

        # Act
        title = extract_title(md)

        # Assert
        self.assertEqual("And a title", title)

    def test_extract_title_no_title(self):
        # Arrange
        md = "## No title"

        # Act
        with self.assertRaises(ValueError) as error:
            extract_title(md)

        # Assert
        self.assertEqual("No title found for markdown", str(error.exception))


if __name__ == "__main__":
    unittest.main()
