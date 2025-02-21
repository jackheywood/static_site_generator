from inline_markdown import extract_markdown_images


def main():
    text = ("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")

    print(extract_markdown_images(text))


if __name__ == '__main__':
    main()
