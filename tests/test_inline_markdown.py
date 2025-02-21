import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links
)


class TestInlineMarkdown(unittest.TestCase):
    def test_text_to_textnodes(self):
        # Arrange
        image_alt = "Image"
        image_url = "https://test.img/image.jpg"
        link_text = "Link"
        link_url = "https://test.link"

        text = ("Text with **bold**, *italic*, `code`, "
                f"![{image_alt}]({image_url}) and "
                f"[{link_text}]({link_url})")

        # Act
        result = text_to_textnodes(text)

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode(image_alt, TextType.IMAGE, image_url),
                TextNode(" and ", TextType.TEXT),
                TextNode(link_text, TextType.LINK, link_url),
            ],
            result,
        )

    def test_split_nodes_delimiter_single_node(self):
        # Arrange
        node = TextNode("Text with **bold phrase** inside", TextType.TEXT)

        # Act
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold phrase", TextType.BOLD),
                TextNode(" inside", TextType.TEXT)
            ],
            result,
        )

    def test_split_nodes_delimiter_end_of_text(self):
        # Arrange
        node = TextNode("Text with code `at the end`", TextType.TEXT)

        # Act
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with code ", TextType.TEXT),
                TextNode("at the end", TextType.CODE)
            ],
            result,
        )

    def test_split_nodes_delimiter_start_of_text(self):
        # Arrange
        node = TextNode("*Italic text* at the start", TextType.TEXT)

        # Act
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)

        # Assert
        self.assertListEqual(
            [
                TextNode("Italic text", TextType.ITALIC),
                TextNode(" at the start", TextType.TEXT)
            ],
            result,
        )

    def test_split_nodes_no_closing_delimiter(self):
        # Arrange
        text = "Text without **closing delimiter"
        node = TextNode(text, TextType.TEXT)

        # Act
        with self.assertRaises(ValueError) as error:
            split_nodes_delimiter([node], "**", TextType.BOLD)

        # Assert
        self.assertEqual(
            f"No closing '**' delimiter found in input text: \"{text}\"",
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
        self.assertListEqual(
            [
                TextNode("code", TextType.CODE),
                TextNode(" with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
                TextNode("!", TextType.TEXT),
            ],
            result,
        )

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
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" section", TextType.TEXT),
                node2,
                node3,
                TextNode("More ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                node5,
            ],
            result,
        )

    def test_split_node_images_single_image(self):
        # Arrange
        alt = "Image"
        url = "https://test.img/image.jpg"
        text = f"Text with ![{alt}]({url}) inside"
        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_image([node])

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode(alt, TextType.IMAGE, url),
                TextNode(" inside", TextType.TEXT)
            ],
            result,
        )

    def test_split_node_images_image_at_start(self):
        # Arrange
        alt = "Image"
        url = "https://test.img/image.jpg"
        text = f"![{alt}]({url}) at start"
        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_image([node])

        # Assert
        self.assertListEqual(
            [
                TextNode(alt, TextType.IMAGE, url),
                TextNode(" at start", TextType.TEXT)
            ],
            result,
        )

    def test_split_node_images_image_at_end(self):
        # Arrange
        alt = "Image"
        url = "https://test.img/image.jpg"
        text = f"Image at end ![{alt}]({url})"
        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_image([node])

        # Assert
        self.assertListEqual(
            [
                TextNode("Image at end ", TextType.TEXT),
                TextNode(alt, TextType.IMAGE, url)
            ],
            result,
        )

    def test_split_node_images_multiple_images(self):
        # Arrange
        alt1 = "Image"
        url1 = "https://test.img/image.jpg"
        alt2 = "Another image"
        url2 = "https://test.img/another.png"

        text = (f"Text with ![{alt1}]({url1}) multiple "
                f"![{alt2}]({url2})![{alt2}]({url2}) images")

        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_image([node])

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode(alt1, TextType.IMAGE, url1),
                TextNode(" multiple ", TextType.TEXT),
                TextNode(alt2, TextType.IMAGE, url2),
                TextNode(alt2, TextType.IMAGE, url2),
                TextNode(" images", TextType.TEXT)
            ],
            result,
        )

    def test_split_node_images_multiple_nodes(self):
        # Arrange
        alt1 = "Image"
        url1 = "https://test.img/image.jpg"
        alt2 = "Another image"
        url2 = "https://test.img/another.png"

        text1 = f"Text with ![{alt1}]({url1}) image"
        text2 = f"Another one ![{alt2}]({url2})"

        node1 = TextNode(text1, TextType.TEXT)
        node2 = TextNode(text2, TextType.TEXT)

        # Act
        result = split_nodes_image([node1, node2])

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode(alt1, TextType.IMAGE, url1),
                TextNode(" image", TextType.TEXT),
                TextNode("Another one ", TextType.TEXT),
                TextNode(alt2, TextType.IMAGE, url2)
            ],
            result,
        )

    def test_split_node_images_not_text_node(self):
        # Arrange
        node = TextNode("Already **a** link", TextType.LINK)

        # Act
        result = split_nodes_image([node])

        # Assert
        self.assertEqual([node], result)

    def test_split_node_images_no_images(self):
        # Arrange
        node = TextNode("Text with no images", TextType.TEXT)

        # Act
        result = split_nodes_image([node])

        # Assert
        self.assertEqual([node], result)

    def test_split_node_links_single_link(self):
        # Arrange
        link = "Link"
        url = "https://link.example"
        text = f"Text with [{link}]({url}) inside"
        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_link([node])

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode(link, TextType.LINK, url),
                TextNode(" inside", TextType.TEXT)
            ],
            result,
        )

    def test_split_node_links_link_at_start(self):
        # Arrange
        link = "Link"
        url = "https://link.example"
        text = f"[{link}]({url}) at start"
        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_link([node])

        # Assert
        self.assertListEqual(
            [
                TextNode(link, TextType.LINK, url),
                TextNode(" at start", TextType.TEXT)
            ],
            result,
        )

    def test_split_node_links_link_at_end(self):
        # Arrange
        link = "Link"
        url = "https://link.example"
        text = f"Link at end [{link}]({url})"
        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_link([node])

        # Assert
        self.assertListEqual(
            [
                TextNode("Link at end ", TextType.TEXT),
                TextNode(link, TextType.LINK, url)
            ],
            result,
        )

    def test_split_node_links_multiple_links(self):
        # Arrange
        link1 = "Link"
        url1 = "https://link.example"
        link2 = "Another link"
        url2 = "https://another.example"

        text = (f"Text with [{link1}]({url1}) multiple "
                f"[{link2}]({url2})[{link2}]({url2}) links")

        node = TextNode(text, TextType.TEXT)

        # Act
        result = split_nodes_link([node])

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode(link1, TextType.LINK, url1),
                TextNode(" multiple ", TextType.TEXT),
                TextNode(link2, TextType.LINK, url2),
                TextNode(link2, TextType.LINK, url2),
                TextNode(" links", TextType.TEXT)
            ],
            result,
        )

    def test_split_node_links_multiple_nodes(self):
        # Arrange
        link1 = "Link"
        url1 = "https://test.img/image.jpg"
        link2 = "Another link"
        url2 = "https://test.img/another.png"

        text1 = f"Text with [{link1}]({url1}) link"
        text2 = f"Another link [{link2}]({url2})"

        node1 = TextNode(text1, TextType.TEXT)
        node2 = TextNode(text2, TextType.TEXT)

        # Act
        result = split_nodes_link([node1, node2])

        # Assert
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode(link1, TextType.LINK, url1),
                TextNode(" link", TextType.TEXT),
                TextNode("Another link ", TextType.TEXT),
                TextNode(link2, TextType.LINK, url2)
            ],
            result,
        )

    def test_split_node_link_not_text_node(self):
        # Arrange
        node = TextNode("Already bold", TextType.BOLD)

        # Act
        result = split_nodes_link([node])

        # Assert
        self.assertEqual([node], result)

    def test_split_node_links_no_links(self):
        # Arrange
        node = TextNode("Text with no links", TextType.TEXT)

        # Act
        result = split_nodes_link([node])

        # Assert
        self.assertEqual([node], result)

    def test_extract_markdown_images(self):
        # Arrange
        alt1 = "Image"
        url1 = "https://test.img/image.jpg"
        alt2 = "Another image"
        url2 = "https://test.img/another.png"
        text = f"[Blah] !(blah) ![{alt1}]({url1}) blah ![{alt2}]({url2}) blah"

        # Act
        result = extract_markdown_images(text)

        # Assert
        self.assertEqual(2, len(result))
        self.assertEqual(((alt1, url1), 15, 51), result[0])
        self.assertEqual(((alt2, url2), 57, 103), result[1])

    def test_extract_markdown_images_not_links(self):
        # Arrange
        alt = "Image"
        url = "https://test.img/image.jpg"
        text = (f"Blah [] blah ![{alt}]({url}) blah "
                "[Link](https://test.link) blah()!")

        # Act
        result = extract_markdown_images(text)
        self.assertEqual(1, len(result))
        self.assertEqual(((alt, url), 13, 49), result[0])

    def test_extract_markdown_links(self):
        # Arrange
        link1 = "Link"
        url1 = "https://test.link"
        link2 = "Another"
        url2 = "https://another.link"

        text = f"Blah ()blah [{link1}]({url1}) blah [{link2}]({url2}) [blah]"

        # Act
        result = extract_markdown_links(text)

        # Assert
        self.assertEqual(2, len(result))
        self.assertEqual(((link1, url1), 12, 37), result[0])
        self.assertEqual(((link2, url2), 43, 74), result[1])

    def test_extract_markdown_links_not_images(self):
        # Arrange
        link = "Link"
        url = "https://test.link"
        text = (f"Blah blah [] () [{link}]({url}) blah ! "
                "![Image](https://another.link) [blah]")

        # Act
        result = extract_markdown_links(text)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(((link, url), 16, 41), result[0])
