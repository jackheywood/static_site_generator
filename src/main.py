from markdown import markdown_to_html_node

md = """
# This is a heading

## This is a subheading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

This is a paragraph with a [link](https://www.google.com)

This is a paragraph with an image ![image](https://i.imgur.com/aKaOqIh.gif)

> This is a multiline
> quote

- This is a list item
- This is another list item

* This is another list
* This is another list item

1. This is a numbered list item
2. This is another numbered list item

```
this is text that _should_ remain
the **same** even though it has markdown
```

"""


def main():
    node = markdown_to_html_node(md)
    print(node.to_html())


if __name__ == '__main__':
    main()
