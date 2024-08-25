from docx import Document
from pdfminer.high_level import extract_text
from .grep import grep
from .show import show

GIGA = 2**30
MEMORY_SIZE = GIGA  # Upper limit of size for loading memory


def search_string_in_file(file_path, search_string,
                          max_length=0, show_text=False, verbose=False, binary=False, memory_size=MEMORY_SIZE):
    """
    Searches for a given string within a file.

    Args:
        file_path (str): The path to the file.
        search_string (str): The string to search for within the file.
        max_length (int, optional): Maximum number of characters to display in the result. Default is 0 (no limit).
        show_text (bool, optional): If True, display the matched line containing the search string. Default is False.
        verbose (bool, optional): If True, print additional information during the search process. Default is False.
        binary (bool, optional): If True, search also in binary files. Default is False.
        memory_size (int, optional): The maximum amount of data to read from a file at a time. Default is MEMORY_SIZE.

    Returns:
        None
    """
    try:
        f = open(file_path, 'r', encoding='utf-8')
    except Exception:
        if binary:
            search_string_in_binary(file_path, search_string, verbose=verbose)
        return
    while True:
        try:
            text = f.read(memory_size)
        except Exception:
            f.close()
            if binary:
                search_string_in_binary(
                    file_path, search_string, verbose=verbose)
            return
        if not text:
            f.close()
            return
        grep(
            file_path,
            text,
            search_string,
            max_length=max_length,
            show_text=show_text)


def search_string_in_binary(file_path, search_string,
                            verbose=False, memory_size=MEMORY_SIZE):
    """
    Searches for a given string within a binary file.

    Args:
        file_path (str): The path to the file.
        search_string (str): The string to search for within the file.
        verbose (bool, optional): If True, print additional information during the search process. Default is False.
        memory_size (int, optional): The maximum amount of data to read from a file at a time. Default is MEMORY_SIZE.

    Returns:
        None
    """
    try:
        with open(file_path, 'rb') as f:
            while True:
                bin = f.read(memory_size)
                if not bin:
                    break
                text = bin.decode('ascii', errors='ignore')
                if search_string in text:
                    print(f'Binary file {file_path} matches.')
                    break
    except Exception as e:
        if verbose:
            print(f"Error reading {file_path}: {e}")


def search_string_in_pdf(file_path, search_string,
                         max_length=0, show_text=False, verbose=False):
    """
    Searches for a given string within a PDF file.

    Args:
        file_path (str): The path to the PDF file.
        search_string (str): The string to search for within the PDF.
        max_length (int, optional): Maximum number of characters to display in the result. Default is 0 (no limit).
        show_text (bool, optional): If True, display the matched line containing the search string. Default is False.
        verbose (bool, optional): If True, print additional information during the search process. Default is False.

    Returns:
        None
    """
    # Display the file path if verbose mode is enabled
    if verbose:
        show(file_path)

    # Read pdf content with pdfminer
    try:
        text = extract_text(file_path)
    except Exception as e:
        if verbose:
            print(f"Error reading {file_path}: {e}")
        return

    # Call grep function to search text
    grep(
        file_path,
        text,
        search_string,
        max_length=max_length,
        show_text=show_text)


def search_string_in_docx(file_path, search_string,
                          max_length=0, show_text=False, verbose=False):
    """
    Searches for a given string within a DOCX file.

    Args:
        file_path (str): The path to the DOCX file.
        search_string (str): The string to search for within the DOCX file.
        max_length (int, optional): Maximum number of characters to display in the result. Default is 0 (no limit).
        show_text (bool, optional): If True, display the matched line containing the search string. Default is False.
        verbose (bool, optional): If True, print additional information during the search process. Default is False.

    Returns:
        None
    """
    # Display the file path if verbose mode is enabled
    if verbose:
        show(file_path)

    # Read DOCX file with docx package
    try:
        doc = Document(file_path)
    except Exception as e:
        if verbose:
            print(f"Error reading {file_path}: {e}")
        return

    # Call grep function to search text
    for paragraph in doc.paragraphs:
        found = grep(
            file_path,
            paragraph.text,
            search_string,
            max_length=max_length,
            show_text=show_text)
        if found and not show_text:
            return
