import sys

from copy_static import copy_files_recursive
from generate_html import generate_pages_recursive

static_dir_path = "static"
content_dir_path = "content"
build_dir_path = "docs"
template_path = "template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Copying static files to public directory...")
    copy_files_recursive(static_dir_path, build_dir_path)

    print(f"Generating HTML pages...")
    generate_pages_recursive(
        content_dir_path,
        template_path,
        build_dir_path,
        basepath,
    )


if __name__ == "__main__":
    main()
