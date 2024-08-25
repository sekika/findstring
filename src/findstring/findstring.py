import os
from .search import search_string_in_file, search_string_in_pdf, search_string_in_docx
from .show import show


def findstring(
        root_dir, search_string, verbose=False, show_text=False, max_length=0, binary=False):
    """
    Recursively searches for a given string within all files in the specified directory.

    Args:
        root_dir (str): The root directory to start searching from.
        search_string (str): The string to search for within the files.
        verbose (bool, optional): If True, print additional information during the search process. Default is False.
        show_text (bool, optional): If True, display the matched line containing the search string. Default is False.
        max_length (int, optional): Maximum number of characters to display in the result. Default is 0 (no limit).
        binary (bool, optional): If True, scan binary files as well. Default is False.

    Returns:
        None
    """
    if verbose:
        show('Checking directory...')
        dirs = os.walk(root_dir)
        len_dirs = sum(1 for _ in dirs)
        count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        if verbose:
            count += 1
            show(f'{count}/{len_dirs}: {dirpath}')
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename.lower().endswith('.pdf'):
                search_string_in_pdf(
                    file_path, search_string, max_length=max_length, show_text=show_text, verbose=verbose)
            elif filename.lower().endswith('.docx'):
                search_string_in_docx(
                    file_path, search_string, max_length=max_length, show_text=show_text, verbose=verbose)
            else:
                search_string_in_file(
                    file_path, search_string, max_length=max_length, show_text=show_text, verbose=verbose, binary=binary)
