import unittest
from unittest.mock import patch
import sys
import io
from src.main import main

class TestBasic(unittest.TestCase):
    def test_initialization(self):
        self.assertTrue(True)

    @patch('sys.argv', ['src/main.py'])
    def test_main_execution(self):
        """Test that main() runs without error and contains new UX elements."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("System", output)
            self.assertIn("Data Source", output)
            self.assertIn("1.", output)
        except Exception as e:
            self.fail(f"main() raised {type(e).__name__} unexpectedly!")
        finally:
            sys.stdout = sys.__stdout__

    @patch('sys.argv', ['src/main.py', '--version'])
    def test_main_version(self):
        """Test that main() exits correctly when called with --version."""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)

    @patch('sys.argv', ['src/main.py'])
    @patch('src.main.get_lib_version')
    @patch('src.main.os.path.isdir')
    @patch('src.main.os.listdir')
    def test_main_status_pending(self, mock_listdir, mock_isdir, mock_get_lib_version):
        """Test that main() displays 'Pending' when dependencies are found but data is missing."""
        mock_get_lib_version.return_value = "1.0.0"
        mock_isdir.return_value = True
        mock_listdir.return_value = [] # Empty directory

        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Pending", output)
            self.assertIn("Data directory is empty", output)
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
