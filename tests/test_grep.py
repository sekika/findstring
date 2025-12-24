import unittest
from unittest.mock import patch
import sys
import io
from findstring.grep import grep, highlight_search_string, colorize_text

class TestGrep(unittest.TestCase):
    """Test cases for grep.py functions."""

    def setUp(self):
        """Redirect stdout to capture print statements for verification."""
        self.capturedOutput = io.StringIO()
        self.sys_stdout = sys.stdout
        sys.stdout = self.capturedOutput

    def tearDown(self):
        """Restore standard output."""
        sys.stdout = self.sys_stdout

    def test_colorize_text_tty(self):
        """Test text colorization when attached to a TTY."""
        with patch('sys.stdout.isatty', return_value=True):
            result = colorize_text("text", "1;31")
            # Expect ANSI escape codes
            self.assertEqual(result, "\033[1;31mtext\033[0m")

    def test_colorize_text_no_tty(self):
        """Test text colorization when NOT attached to a TTY (plain text)."""
        with patch('sys.stdout.isatty', return_value=False):
            result = colorize_text("text", "1;31")
            # Expect plain text
            self.assertEqual(result, "text")

    def test_highlight_search_string(self):
        """Test if the search string is correctly wrapped in color codes."""
        # Force isatty to True to ensure colors are applied for the test
        with patch('sys.stdout.isatty', return_value=True):
            line = "Hello world example."
            search = "world"
            result = highlight_search_string(line, search)
            # Check if 'world' is surrounded by ANSI codes
            self.assertIn(f"\033[1;31m{search}\033[0m", result)

    def test_grep_found_no_text(self):
        """Test grep finding a string but NOT showing the text line (default behavior)."""
        file_path = "test.txt"
        text = "This is a sample line."
        search = "sample"
        
        found = grep(file_path, text, search, show_text=False)
        
        self.assertTrue(found)
        # Should print the file path only
        self.assertEqual(self.capturedOutput.getvalue().strip(), file_path)

    def test_grep_not_found(self):
        """Test grep when the string is not in the text."""
        found = grep("test.txt", "content", "missing")
        self.assertFalse(found)
        self.assertEqual(self.capturedOutput.getvalue(), "")

    def test_grep_show_text(self):
        """Test grep showing the matched line with highlighting."""
        file_path = "test.txt"
        text = "Target line."
        search = "Target"

        with patch('sys.stdout.isatty', return_value=True):
            grep(file_path, text, search, show_text=True)
            
        output = self.capturedOutput.getvalue().strip()
        # Should contain filename and highlighted content
        self.assertIn(file_path, output)
        self.assertIn("\033[1;31mTarget\033[0m", output)

    def test_grep_max_length(self):
        """Test the truncation logic (context display) when max_length is set."""
        file_path = "test.txt"
        # Create a long string
        text = "prefix " + "A" * 50 + " match " + "B" * 50 + " suffix"
        search = "match"
        
        # Limit length to roughly the size of 'match' + some padding
        grep(file_path, text, search, show_text=True, max_length=20)
        
        output = self.capturedOutput.getvalue().strip()
        # Ensure the whole line isn't printed (prefix should be cut off)
        self.assertNotIn("prefix", output)
        self.assertIn("match", output)

if __name__ == '__main__':
    unittest.main()
