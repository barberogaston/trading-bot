import os


def get_data_folder_path() -> str:
    """Returns the data folder path."""
    return os.path.abspath(os.path.dirname(__file__))
