import unittest
import os
import tempfile
import io
import sys
from unittest.mock import patch, MagicMock
from findstring.search import (
    search_string_in_file, 
    search_string_in_pdf, 
    search_string_in_docx
)
from findstring.findstring import findstring

class TestSearch(unittest.TestCase):
    """Test cases for search logic and integration."""

    def setUp(self):
        """Redirect stdout."""
        self.capturedOutput = io.StringIO()
        self.sys_stdout = sys.stdout
        sys.stdout = self.capturedOutput
        
        # Create a temporary directory for file tests
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        sys.stdout = self.sys_stdout
        self.test_dir.cleanup()

    def create_file(self, filename, content, binary=False):
        """Helper to create files in the temp directory."""
        path = os.path.join(self.test_dir.name, filename)
        mode = 'wb' if binary else 'w'
        encoding = None if binary else 'utf-8'
        with open(path, mode, encoding=encoding) as f:
            f.write(content)
        return path

    def test_search_string_in_file_found(self):
        """Test searching in a standard text file."""
        path = self.create_file("test.txt", "Hello World")
        search_string_in_file(path, "World")
        self.assertIn(path, self.capturedOutput.getvalue())

    def test_search_string_in_file_not_found(self):
        """Test searching for a non-existent string."""
        path = self.create_file("test.txt", "Hello World")
        search_string_in_file(path, "Banana")
        self.assertEqual(self.capturedOutput.getvalue(), "")

    def test_search_string_in_binary_file(self):
        """Test searching in a binary file when binary=True."""
        # FIX: Use \xFF which is invalid in UTF-8. 
        # This ensures f.read() raises UnicodeDecodeError, triggering the exception handler.
        path = self.create_file("bin.dat", b"\xFF\xFFFoundMe\x00", binary=True)
        
        # Case 1: binary=False
        # Behavior: read fails, exception caught, simply returns (no output).
        search_string_in_file(path, "FoundMe", binary=False)
        self.assertEqual(self.capturedOutput.getvalue(), "")

        # Case 2: binary=True
        # Behavior: read fails, exception caught, switches to binary search logic, finds string.
        search_string_in_file(path, "FoundMe", binary=True)
        self.assertIn(f"Binary file {path} matches", self.capturedOutput.getvalue())

    @patch('findstring.search.extract_text')
    def test_search_string_in_pdf(self, mock_extract_text):
        """Test PDF search by mocking pdfminer."""
        # Mock the content returned by pdfminer
        mock_extract_text.return_value = "This is a PDF content line."
        path = "dummy.pdf"
        
        search_string_in_pdf(path, "content", verbose=False)
        
        # Check if the grep logic was triggered (filename printed)
        self.assertIn(path, self.capturedOutput.getvalue())

    @patch('findstring.search.Document')
    def test_search_string_in_docx(self, mock_document_cls):
        """Test DOCX search by mocking python-docx."""
        # Mock the Document object and its paragraphs
        mock_doc = MagicMock()
        mock_paragraph = MagicMock()
        mock_paragraph.text = "This is a DOCX paragraph."
        mock_doc.paragraphs = [mock_paragraph]
        mock_document_cls.return_value = mock_doc
        
        path = "dummy.docx"
        search_string_in_docx(path, "paragraph", verbose=False)
        
        self.assertIn(path, self.capturedOutput.getvalue())

    def test_findstring_integration(self):
        """Test the main recursive walker function."""
        # Create nested structure
        sub_dir = os.path.join(self.test_dir.name, "subdir")
        os.mkdir(sub_dir)
        
        self.create_file("root.txt", "root match")
        self.create_file("subdir/child.txt", "child match")
        self.create_file("subdir/nomatch.txt", "nothing here")

        # Run findstring on the temp root directory
        findstring(self.test_dir.name, "match")

        output = self.capturedOutput.getvalue()
        # Verify both files are found
        self.assertIn("root.txt", output)
        self.assertIn("child.txt", output)
        # Verify the non-matching file is not listed
        self.assertNotIn("nomatch.txt", output)

if __name__ == '__main__':
    unittest.main()
