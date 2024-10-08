# ccrepo/api.py

# Description: This file contains the main API functions for the ccrepo package.

import logging
import os

import colorlog
import requests
from tqdm import tqdm


def _set_logger(filename: str = None):
    """
    Initialises Python logging module with a custom format and log level.
    """
    ccrepo_logger = logging.getLogger("ccrepo")
    ccrepo_logger.setLevel(logging.INFO)

    log_format = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"

    bold = "\033[1m"

    colorlog_format = f"{bold} " "%(log_color)s " f"{log_format}"

    colorlog.basicConfig(format=colorlog_format)

    if filename is not None:
        fh = logging.FileHandler(filename)
        fh.setLevel(level)
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        ccrepo_logger.addHandler(fh)

    return ccrepo_logger


def fetch_file_from_repo():
    """
    Fetch a file from the specified GitHub repository using a personal access token,
    with a progress bar.

    Parameters:
        token (str): The personal access token for authentication.

    Returns:
        str: The content of the file.
    """

    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_filepath = os.path.join(script_dir, "data", "cc-basis-catalogue.txt")

    repo_url = "https://raw.githubusercontent.com/Sheffield-Theoretical-Chemistry/ccrepo-raw/main/cc-basis-catalogue.txt"
    # headers = {"Authorization": f"token {token}"}
    try:
        response = requests.get(repo_url, stream=True)

        if response.status_code == 200:
            total_length = int(response.headers.get("content-length", 0))
            if total_length == 0:
                raise ValueError("Failed to retrieve content length for the file.")

            content = []
            with tqdm(
                total=total_length,
                unit="B",
                unit_scale=True,
                desc="Retrieving basis set catalogue",
                ncols=100,
                ascii=True,
                leave=True,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        content.append(chunk)
                        pbar.update(len(chunk))

            return b"".join(content).decode("utf-8")
        else:
            ccrepo_logger.warning(
                "Unable to access online repository, using local copy. Note, this may be out of date."
            )
            with open(data_filepath, "r") as catalogue:
                return catalogue.read()
            # response.raise_for_status()
    except Exception as e:
        print(e)
        ccrepo_logger.warning(
            "Unable to access online repository, using local copy. Note, this may be out of date."
        )
        with open(data_filepath, "r") as catalogue:
            return catalogue.read()


ccrepo_logger = _set_logger()
