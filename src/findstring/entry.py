"""
Entry point of findstring
"""
import argparse
import pkg_resources
from .findstring import findstring
from .show import show


def entry():
    """
    Entry point for the findstring program. This function parses the command-line arguments
    and invokes the find_files_with_string function with the appropriate parameters.

    Args:
        None

    Returns:
        None
    """
    # Argument parsing and handling for the findstring program
    version = pkg_resources.get_distribution('findstring').version
    parser = argparse.ArgumentParser(
        description=f"findstring {version} - search for a string in files recursively including pdf and docx files. See https://pypi.org/project/findstring")
    parser.add_argument(
        "search_string",
        help="string to search for in files")
    parser.add_argument(
        '-b',
        '--binary',
        action='store_true',
        help='scan binary files')
    parser.add_argument(
        "-d",
        "--directory",
        nargs="?",
        default=".",
        help="root directory to start searching from (default is current directory)")
    parser.add_argument(
        "-l",
        "--max_length",
        type=int,
        nargs="?",
        default=0,
        help="maximum numbers of characters shown as a result (default is 0 = no limit)")
    parser.add_argument(
        '-t',
        '--text',
        action='store_true',
        help='show matched lines')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')

    args = parser.parse_args()
    if args.max_length > 0:
        args.text = True

    findstring(
        args.directory,
        args.search_string,
        verbose=args.verbose,
        show_text=args.text,
        max_length=args.max_length,
        binary=args.binary)

    if args.verbose:
        show('')
