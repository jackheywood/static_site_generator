import os

from markdown import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path}"
        f" using template {template_path}"
    )

    markdown = read_file(from_path)
    template = read_file(template_path)

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)

    write_file(dest_path, html)


def read_file(path):
    if not os.path.exists(path):
        raise IOError(f"File '{path}' does not exist")
    if not os.path.isfile(path):
        raise IOError(f"'{path}' is not a file")
    with open(path, "r") as f:
        return f.read()


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
