import unittest
from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Arrange
        markdown = (
            "# Heading\n"
            "\n"
            "Paragraph of text.\n"
            "\n"
            "* List 1\n"
            "* List 2\n"
            "* List 3")

        # Act
        result = markdown_to_blocks(markdown)

        # Assert
        self.assertListEqual(
            [
                "# Heading",
                "Paragraph of text.",
                "* List 1\n* List 2\n* List 3",
            ],
            result,
        )

    def test_markdown_to_blocks_trims_whitespace(self):
        # Arrange
        markdown = (
            "   # Block with whitespace   \n"
            "\n"
            "  ## Another block with whitespace    ")

        # Act
        result = markdown_to_blocks(markdown)

        # Assert
        self.assertListEqual(
            [
                "# Block with whitespace",
                "## Another block with whitespace",
            ],
            result,
        )

    def test_markdown_to_blocks_removes_empty_blocks(self):
        # Arrange
        markdown = (
            "# Heading\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "Paragraph of text."
        )

        # Act
        result = markdown_to_blocks(markdown)

        # Assert
        self.assertListEqual(
            [
                "# Heading",
                "Paragraph of text.",
            ],
            result,
        )

    def test_markdown_to_blocks_single_block(self):
        # Arrange
        markdown = "# Heading"

        # Act
        result = markdown_to_blocks(markdown)

        # Assert
        self.assertListEqual([markdown], result)

    def test_markdown_to_blocks_empty_markdown(self):
        # Act
        result = markdown_to_blocks("")

        # Assert
        self.assertListEqual([], result)


if __name__ == "__main__":
    unittest.main()
