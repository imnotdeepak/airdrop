import os


def safe_delete_file(file: str):
    """Deletes a given file without the possibility of raising an error.
    """

    if os.path.exists(file):
        os.remove(file)
