import os

from markdown import markdown_to_html_node, extract_title


def generate_pages_recursive(source_dir_path, template_path, dest_dir_path):
    if not os.path.exists(source_dir_path):
        raise IOError(f"Source directory '{source_dir_path}' does not exist")

    for entry in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, entry)
        dest_path = os.path.join(dest_dir_path, os.path.splitext(entry)[0])

        if os.path.isdir(source_path):
            generate_pages_recursive(source_path, template_path, dest_path)
        elif entry.endswith(".md") and os.path.isfile(source_path):
            generate_page(source_path, template_path, dest_path + ".html")


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} -> {dest_path}")

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
