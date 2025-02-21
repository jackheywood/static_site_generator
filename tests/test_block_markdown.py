import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type


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

    def test_block_to_block_type_code(self):
        # Arrange
        block = "```\nprint('Hello, World!')\n```"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.CODE, result)

    def test_block_to_block_type_invalid_code_no_newline_at_end(self):
        # Arrange
        block = "```\nprint('Hello, World!')```"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_invalid_code_no_closing_backticks(self):
        # Arrange
        block = "```\nprint('Hello, World!')\n"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_heading(self):
        # Arrange
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]

        # Act
        results = [block_to_block_type(block) for block in blocks]

        # Assert
        for result in results:
            self.assertEqual(BlockType.HEADING, result)

    def test_block_to_block_type_invalid_heading(self):
        # Arrange
        block = "####### Heading 7"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_quote(self):
        # Arrange
        block = "> This is a quote\n>spread across\n> multiple lines"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.QUOTE, result)

    def test_block_to_block_type_invalid_quote(self):
        # Arrange
        block = "> This is a quote\nwith a quote character\n> missing"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_unordered_list_asterisks(self):
        # Arrange
        block = "* Item 1\n* Item 2\n* Item 3\n* Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.ULIST, result)

    def test_block_to_block_type_unordered_list_hyphens(self):
        # Arrange
        block = "- Item 1\n- Item 2\n- Item 3\n- Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.ULIST, result)

    def test_block_to_block_type_invalid_unordered_list_missing_space(self):
        # Arrange
        block = "* Item 1\n*Missing space\n* Item 3\n* Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_invalid_unordered_list_mixed_character(self):
        # Arrange
        block = "- Item 1\n* Item 2\n* Item 3\n- Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_invalid_unordered_list_wrong_character(self):
        # Arrange
        block = "- Item 1\n# Wrong character\n- Item 3\n- Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_ordered_list(self):
        # Arrange
        block = "1. Item 1\n2. Item 2\n3. Item 3\n4. Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.OLIST, result)

    def test_block_to_block_type_invalid_ordered_list_starting_at_zero(self):
        # Arrange
        block = "0. Item 1\n1. Item 2\n2. Item 3\n3. Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_invalid_ordered_list_wrong_sequence(self):
        # Arrange
        block = "1. Item 1\n1. Item 2\n3. Item 3\n2. Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_invalid_ordered_list_missing_space(self):
        # Arrange
        block = "1. Item 1\n2. Item 2\n3.Missing space\n4. Item 4"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_invalid_ordered_list_wrong_character(self):
        # Arrange
        block = "1. Item 1\n2. Item 2\n3. Missing space\nX. Wrong character"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)

    def test_block_to_block_type_paragraph(self):
        # Arrange
        block = "Paragraph of text\nspread across\nmultiple lines"

        # Act
        result = block_to_block_type(block)

        # Assert
        self.assertEqual(BlockType.PARAGRAPH, result)


if __name__ == "__main__":
    unittest.main()
