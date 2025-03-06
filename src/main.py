from copy_static import copy_files_recursive
from generate_html import generate_pages_recursive

static_dir_path = "static"
content_dir_path = "content"
public_dir_path = "public"
template_path = "template.html"


def main():
    print("Copying static files to public directory...")
    copy_files_recursive(static_dir_path, public_dir_path)

    print(f"Generating HTML pages...")
    generate_pages_recursive(content_dir_path, template_path, public_dir_path)


if __name__ == "__main__":
    main()
