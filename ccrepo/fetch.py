# ccrepo_basis_set/fetch.py
import requests
from tqdm import tqdm
from typing import Union


def fetch_file_from_repo(token):
    """
    Fetch a file from the specified GitHub repository using a personal access token,
    with a progress bar.

    Parameters:
        token (str): The personal access token for authentication.

    Returns:
        str: The content of the file.
    """
    repo_url = "https://raw.githubusercontent.com/stedonnelly/ccrepo-raw/main/cc-basis-catalogue.txt"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(repo_url, headers=headers, stream=True)

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
        response.raise_for_status()


def get_basis_set_block(
    content: str, elements: Union[str, list], basis_set_name: str
) -> str:
    """
    Extract the basis set block for a given element and basis set name.

    Parameters:
        content (str): The content of the basis set file.
        element (list or str): The element symbol.
        basis_set_name (str): The name of the basis set.

    Returns:
        str: The block of the basis set for the specified element and basis set name.
    """
    lines = content.split("\n")
    blocks = []
    capture = False
    current_block = []

    available_basis = []

    for line in lines:
        if any(line.startswith(f"{element}:{basis_set_name}:") for element in elements):
            available_basis.append(line.split(':')[0])
            capture = True
            current_block = [line]
        elif capture:
            if line.strip() == "":
                capture = False
                blocks.append("\n".join(current_block))
                current_block = []
            else:
                current_block.append(line)

    # Append the last captured block if it wasn't appended yet
    if capture and current_block:
        blocks.append("\n".join(current_block))

    for element in elements:
        if element not in available_basis:
            print(
                f"No {basis_set_name} found for element {element} in the ccRepo catalogue."
            )
    unavailable_basis = [element for element in elements if element not in available_basis]
    if blocks:
        print(f"Found {basis_set_name} for element(s) {','.join(available_basis)} in the ccRepo catalogue.")
        if unavailable_basis:
            print(f"No {basis_set_name} found for element(s) {','.join(unavailable_basis)} in the ccRepo catalogue.")
        return "\n\n".join(blocks)
    else:
        raise ValueError(
            f"No basis set blocks found for elements {elements} with basis set {basis_set_name}"
        )

