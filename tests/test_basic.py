import unittest
from unittest.mock import patch
import sys
from src.main import main

class TestBasic(unittest.TestCase):
    def test_initialization(self):
        self.assertTrue(True)

    @patch('sys.argv', ['src/main.py'])
    def test_main_execution(self):
        """Test that main() runs without error when called with no arguments."""
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised {type(e).__name__} unexpectedly!")

    @patch('sys.argv', ['src/main.py', '--version'])
    def test_main_version(self):
        """Test that main() exits correctly when called with --version."""
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)

if __name__ == '__main__':
    unittest.main()
