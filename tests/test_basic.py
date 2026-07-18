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
            self.assertIn("Dependencies", output)
            self.assertIn("1.", output)
            # Check for new dynamic status indicators
            self.assertIn("[PEND]", output)
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

    @patch('sys.argv', ['src/main.py', '--init'])
    @patch('os.makedirs')
    @patch('builtins.open')
    def test_main_init(self, mock_open, mock_makedirs):
        """Test that main() behaves correctly when called with --init."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            self.assertIn("Initialization complete!", output)
            self.assertIn("Created data/ directory.", output)
            self.assertIn("Populated data/products.csv", output)
            mock_makedirs.assert_called_once_with("data", exist_ok=True)
            mock_open.assert_called_once()
        except Exception as e:
            self.fail(f"main() raised {type(e).__name__} unexpectedly!")
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
