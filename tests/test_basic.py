import unittest
from unittest.mock import patch, MagicMock
import sys
import io

class TestBasic(unittest.TestCase):
    def test_initialization(self):
        self.assertTrue(True)

    @patch('sys.exit')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_missing_dependencies(self, mock_stdout, mock_exit):
        # Simulate missing pandas dependency
        with patch.dict('sys.modules', {'pandas': None}):
            # Re-import main to ensure it uses the mocked sys.modules
            if 'src.main' in sys.modules:
                del sys.modules['src.main']
            from src.main import main
            main()

            output = mock_stdout.getvalue()
            self.assertIn("✨ Welcome to Smart Product Analysis! ✨", output)
            self.assertIn("pip install -r requirements.txt", output)
            mock_exit.assert_called_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_success(self, mock_stdout):
        # Simulate successful dependency import
        mock_pandas = MagicMock()
        mock_numpy = MagicMock()

        with patch.dict('sys.modules', {'pandas': mock_pandas, 'numpy': mock_numpy}):
            # Re-import main to ensure it uses the mocked sys.modules
            if 'src.main' in sys.modules:
                del sys.modules['src.main']
            from src.main import main
            main()

            output = mock_stdout.getvalue()
            self.assertIn("Smart Product Analysis Initialized 🚀", output)

if __name__ == '__main__':
    unittest.main()
