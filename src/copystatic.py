import os
import shutil


def copy_files_recursive(source, dest):
    if not os.path.exists(source):
        raise IOError(f"Source directory '{source}' does not exist")

    create_clean_directory(dest)

    for entry in os.listdir(source):
        source_path = os.path.join(source, entry)
        dest_path = os.path.join(dest, entry)
        copy_item(source_path, dest_path)


def create_clean_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def copy_item(source, dest):
    print(f"  * {source} -> {dest}")
    if os.path.isfile(source):
        shutil.copy(source, dest)
    elif os.path.isdir(source):
        copy_files_recursive(source, dest)
    else:
        raise IOError(
            f"Source item '{source}' is neither a file nor a directory"
        )
