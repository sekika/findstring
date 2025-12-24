import unittest
from unittest.mock import patch
import sys
from findstring.entry import entry

class TestEntry(unittest.TestCase):
    """Test cases for the CLI entry point."""

    @patch('findstring.entry.findstring')
    @patch('findstring.entry.version', return_value='1.0.0')
    def test_entry_arguments(self, mock_version, mock_findstring):
        """Test that command line arguments are correctly parsed and passed to findstring."""
        
        # Simulate command line arguments: findstring -v -t "search_term"
        test_args = ['findstring', '-v', '-t', 'search_term']
        
        with patch.object(sys, 'argv', test_args):
            entry()
            
            # Verify findstring was called with expected arguments
            mock_findstring.assert_called_once_with(
                ".",            # Default directory
                "search_term",  # Search string
                verbose=True,   # -v flag
                show_text=True, # -t flag
                max_length=0,   # Default
                binary=False    # Default
            )

    @patch('findstring.entry.findstring')
    @patch('findstring.entry.version', return_value='1.0.0')
    def test_entry_directory_argument(self, mock_version, mock_findstring):
        """Test specifying a custom directory."""
        
        test_args = ['findstring', '-d', '/tmp', 'keyword']
        
        with patch.object(sys, 'argv', test_args):
            entry()
            
            mock_findstring.assert_called_once_with(
                "/tmp",
                "keyword",
                verbose=False,
                show_text=False,
                max_length=0,
                binary=False
            )

    @patch('findstring.entry.findstring')
    @patch('findstring.entry.version', return_value='1.0.0')
    def test_entry_max_length_sets_text(self, mock_version, mock_findstring):
        """Test that setting max_length (-l) automatically enables show_text."""
        
        # -l implies -t logic in entry.py
        test_args = ['findstring', '-l', '50', 'keyword']
        
        with patch.object(sys, 'argv', test_args):
            entry()
            
            mock_findstring.assert_called_once()
            args, kwargs = mock_findstring.call_args
            
            # Verify max_length is passed
            self.assertEqual(kwargs['max_length'], 50)
            # Verify show_text is forced to True
            self.assertTrue(kwargs['show_text'])

if __name__ == '__main__':
    unittest.main()
