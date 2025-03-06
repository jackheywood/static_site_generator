from copy_static import copy_files_recursive
from generate_html import generate_page


def main():
    print("Copying static files to public directory...")
    copy_files_recursive("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
