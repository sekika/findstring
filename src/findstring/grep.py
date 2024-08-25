import os
import re
import sys


def grep(file_path, text, search_string,
         max_length=0, show_text=False):
    """
    Searches for a string within a block of text, optionally displaying the surrounding context.

    Args:
        file_path (str): The path of the file being searched.
        text (str): The text content to search within.
        search_string (str): The string to search for.
        max_length (int, optional): Maximum number of characters to display in the result. Default is 0 (no limit).
        show_text (bool, optional): If True, display the matched line containing the search string. Default is False.
        binary (bool, optional): If True, indicate that the file is binary. Default is False.

    Returns:
        bool: If True, indicate that the string is found.
    """
    # Check if the string is present in the text and handle the output
    # accordingly
    for line in text.splitlines():
        if search_string in line:
            if show_text:
                find_contexts(
                    file_path,
                    line,
                    search_string,
                    max_length=max_length)
            else:
                print(file_path)
                return True
    return False


def find_contexts(file_path, line, search_string, max_length=0):
    """
    Displays the context around the matched search string within a line of text.

    Args:
        file_path (str): The path of the file where the match was found.
        line (str): The line of text containing the search string.
        search_string (str): The string that was searched for.
        max_length (int, optional): Maximum number of characters to display in the context. Default is 0 (no limit).

    Returns:
        None
    """
    if max_length == 0 or (len(line) <= max_length and len(
            line) < len(search_string) + 10):
        line = highlight_search_string(line, search_string)
        print(f'{file_path}:{line}')
        return
    context_size = (max_length - len(search_string)) // 2
    pattern = re.escape(search_string)
    matches = re.finditer(pattern, line)

    for match in matches:
        start = match.start()
        end = match.end()
        context_start = max(0, start - context_size)
        context_end = min(len(line), end + context_size)
        context = line[context_start:context_end]
        context = highlight_search_string(context, search_string)
        print(f'{file_path}:{context}')


def highlight_search_string(line, search_string):
    """
    Highlights all occurrences of the search string within a line of text by adding color codes.

    Args:
        line (str): The line of text in which to highlight the search string.
        search_string (str): The string to be highlighted within the line.

    Returns:
        str: The line with the search string highlighted using terminal color codes.
    """
    color_code = get_mt_value()
    colored_line = re.sub(
        f'({re.escape(search_string)})',
        lambda match: colorize_text(match.group(1), color_code),
        line
    )
    return colored_line


def colorize_text(text, color_code):
    """
    Applies a terminal color code to a given text if the output is a terminal.

    Args:
        text (str): The text to colorize.
        color_code (str): The terminal color code to apply.

    Returns:
        str: The colorized text if the output is a terminal; otherwise, returns the original text.
    """
    if not sys.stdout.isatty():
        return text
    return f'\033[{color_code}m{text}\033[0m'


def get_mt_value(default_value='1;31'):
    """
    Retrieves the color code for highlighting from the GREP_COLORS environment variable, or uses a default value.

    Args:
        default_value (str, optional): The default color code to use if GREP_COLORS is not set. Default is '1;31' (red).

    Returns:
        str: The color code to be used for highlighting text.
    """
    grep_colors = os.getenv('GREP_COLORS', '')
    mt_value = default_value
    # If the GREP_COLORS variable contains a 'mt=' value, extract and use it
    if 'mt=' in grep_colors:
        mt_value = grep_colors.split('mt=')[1].split(':')[0]
    return mt_value
