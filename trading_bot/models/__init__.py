import os


def get_models_folder_path() -> str:
    """Returns the models folder path."""
    return os.path.abspath(os.path.dirname(__file__))
