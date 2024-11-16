import os

DOWNLOAD_PATH = "downloads/"


def get_download_path() -> str:
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    return DOWNLOAD_PATH
