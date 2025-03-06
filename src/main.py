from copystatic import copy_files_recursive


def main():
    print("Copying static files to public directory...")
    copy_files_recursive("static", "public")


if __name__ == "__main__":
    main()
