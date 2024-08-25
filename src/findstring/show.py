import shutil


def show(text):
    """
    Prints the provided text in a truncated form if it exceeds the specified character limit.

    Args:
        text (str): The text to display.

    Returns:
        None
    """
    # Truncate the text if it exceeds the character limit and print it
    default_terminal_size = (80, 20)
    terminal_size = shutil.get_terminal_size(default_terminal_size)
    chars = terminal_size[0] - 1
    showtext = text
    if len(text.encode('utf-8')) > chars:
        showtext = text.encode(
            'utf-8')[:chars - 3].decode('utf-8', 'ignore') + '...'
    print(f'{" "*chars}\r{showtext}\r', end='')
