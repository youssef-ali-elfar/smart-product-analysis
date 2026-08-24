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
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_main_init(self, mock_getsize, mock_isfile, mock_open, mock_makedirs):
        """Test that main() behaves correctly when called with --init."""
        mock_isfile.return_value = False
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

    @patch('sys.argv', ['src/main.py', '--init'])
    @patch('os.makedirs')
    @patch('builtins.open')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('sys.stdin')
    def test_main_init_overwrite_confirm(self, mock_stdin, mock_getsize, mock_isfile, mock_open, mock_makedirs):
        """Test that --init prompts for confirmation if products.csv exists and contains data."""
        mock_isfile.return_value = True
        mock_getsize.return_value = 100
        mock_stdin.isatty.return_value = True

        # Test case where user says No
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='n'):
            main()
            output = captured_output.getvalue()
            self.assertIn("Initialization aborted.", output)
            mock_open.assert_not_called()

        # Test case where user says Yes
        mock_open.reset_mock()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='y'):
            main()
            output = captured_output.getvalue()
            self.assertIn("Initialization complete!", output)
            mock_open.assert_called_once()

    @patch('sys.argv', ['src/main.py'])
    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('builtins.open')
    @patch('sys.stdin')
    def test_interactive_onboarding_prompt(self, mock_stdin, mock_open, mock_makedirs, mock_isdir, mock_get_lib_version):
        """Test interactive onboarding prompt triggers and behaves correctly when data dir is missing."""
        mock_get_lib_version.return_value = "1.2.3"  # All libs found
        mock_isdir.return_value = False  # Data dir missing
        mock_stdin.isatty.return_value = True

        # Test user declines onboarding prompt
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='n') as mock_input:
            main()
            output = captured_output.getvalue()
            mock_input.assert_called_once()
            self.assertIn("Would you like to initialize the workspace with sample data now?", mock_input.call_args[0][0])
            self.assertIn("Onboarding declined.", output)
            self.assertIn("manually create", output)
            self.assertNotIn("Initialization complete!", output)
            mock_open.assert_not_called()

        # Test KeyboardInterrupt during onboarding prompt
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', side_effect=KeyboardInterrupt) as mock_input:
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 0)
            output = captured_output.getvalue()
            self.assertIn("Onboarding interrupted. Exiting gracefully...", output)

        # Test user accepts onboarding prompt
        mock_open.reset_mock()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', return_value='yes') as mock_input:
            main()
            output = captured_output.getvalue()
            mock_input.assert_called_once()
            self.assertIn("Would you like to initialize the workspace with sample data now?", mock_input.call_args[0][0])
            self.assertIn("Initialization complete!", output)
            self.assertIn("Refreshing workspace status...", output)
            mock_open.assert_called_once()

    @patch('sys.argv', ['src/main.py', '--init'])
    @patch('os.makedirs')
    @patch('builtins.open')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('sys.stdin')
    def test_init_overwrite_help(self, mock_stdin, mock_getsize, mock_isfile, mock_open, mock_makedirs):
        """Test that typing 'help' in the --init overwrite prompt displays details and re-prompts."""
        mock_isfile.return_value = True
        mock_getsize.return_value = 100
        mock_stdin.isatty.return_value = True

        captured_output = io.StringIO()
        sys.stdout = captured_output
        # Mock side_effect to input 'help' (which should re-prompt) then 'n' (to abort)
        with patch('builtins.input', side_effect=['help', 'n']) as mock_input:
            main()
            output = captured_output.getvalue()
            self.assertEqual(mock_input.call_count, 2)
            self.assertIn("Help - Overwriting Data:", output)
            self.assertIn("clean sample mock data", output)
            self.assertIn("Initialization aborted.", output)
            mock_open.assert_not_called()

    @patch('sys.argv', ['src/main.py'])
    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('builtins.open')
    @patch('sys.stdin')
    def test_interactive_onboarding_help(self, mock_stdin, mock_open, mock_makedirs, mock_isdir, mock_get_lib_version):
        """Test that typing '?' in the onboarding prompt displays details and re-prompts."""
        mock_get_lib_version.return_value = "1.2.3"  # All libs found
        mock_isdir.return_value = False  # Data dir missing
        mock_stdin.isatty.return_value = True

        captured_output = io.StringIO()
        sys.stdout = captured_output
        # Mock side_effect to input '?' (which should re-prompt) then 'y' (to accept and initialize)
        with patch('builtins.input', side_effect=['?', 'y']) as mock_input:
            main()
            output = captured_output.getvalue()
            self.assertEqual(mock_input.call_count, 2)
            self.assertIn("Help - Workspace Onboarding:", output)
            self.assertIn("lacks sample product files in the data directory", output)
            self.assertIn("Initialization complete!", output)
            mock_open.assert_called_once()

    @patch('sys.argv', ['src/main.py', '--init'])
    @patch('os.makedirs')
    @patch('builtins.open')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('sys.stdin')
    def test_init_overwrite_invalid_input_reprompt(self, mock_stdin, mock_getsize, mock_isfile, mock_open, mock_makedirs):
        """Test that typing an invalid choice in the --init prompt displays error and re-prompts."""
        mock_isfile.return_value = True
        mock_getsize.return_value = 100
        mock_stdin.isatty.return_value = True

        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', side_effect=['invalid_choice', 'n']) as mock_input:
            main()
            output = captured_output.getvalue()
            self.assertEqual(mock_input.call_count, 2)
            self.assertIn("Unrecognized option: 'invalid_choice'", output)
            self.assertIn("Initialization aborted.", output)
            mock_open.assert_not_called()

    @patch('sys.argv', ['src/main.py'])
    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('builtins.open')
    @patch('sys.stdin')
    def test_onboarding_invalid_input_reprompt(self, mock_stdin, mock_open, mock_makedirs, mock_isdir, mock_get_lib_version):
        """Test that typing an invalid choice in the onboarding prompt displays error and re-prompts."""
        mock_get_lib_version.return_value = "1.2.3"  # All libs found
        mock_isdir.return_value = False  # Data dir missing
        mock_stdin.isatty.return_value = True

        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', side_effect=['typo', 'n']) as mock_input:
            main()
            output = captured_output.getvalue()
            self.assertEqual(mock_input.call_count, 2)
            self.assertIn("Unrecognized option: 'typo'", output)
            self.assertIn("Onboarding declined.", output)
            mock_open.assert_not_called()

    @patch('sys.argv', ['src/main.py'])
    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('builtins.open')
    def test_missing_values_detection_and_tip(self, mock_open, mock_getsize, mock_isfile, mock_listdir, mock_isdir, mock_get_lib_version):
        """Test that missing values in CSV dataset are correctly detected and prompt corresponding warning and cleaning tip."""
        mock_get_lib_version.return_value = "1.2.3"  # All libs found
        mock_isdir.return_value = True
        mock_listdir.return_value = ["dirty.csv"]
        mock_isfile.return_value = True
        mock_getsize.return_value = 120

        # CSV data with 4 missing values
        csv_content = "id,name,category,price,stock\n1,Smart Watch,,199.99,\n2,,Electronics,79.99,120\n3,Running Shoes,Apparel,,85"
        mock_open.return_value = io.StringIO(csv_content)

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        output = captured_output.getvalue()

        self.assertIn("dirty.csv", output)
        self.assertIn("4 missing values", output)
        self.assertIn("Detected 4 missing values in name, category, price, and stock in your dataset. Proceed to Stage 2: Data Cleaning to handle them!", output)

    @patch('sys.argv', ['src/main.py'])
    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('builtins.open')
    def test_zero_row_csv_detection_and_tip(self, mock_open, mock_getsize, mock_isfile, mock_listdir, mock_isdir, mock_get_lib_version):
        """Test that CSV datasets with headers but 0 data rows display warning badge and tip."""
        mock_get_lib_version.return_value = "1.2.3"
        mock_isdir.return_value = True
        mock_listdir.return_value = ["empty_header.csv"]
        mock_isfile.return_value = True
        mock_getsize.return_value = 50

        # CSV with header only (0 data rows)
        csv_content = "id,name,category,price,stock\n"
        mock_open.return_value = io.StringIO(csv_content)

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        output = captured_output.getvalue()

        self.assertIn("empty_header.csv", output)
        self.assertIn("0 data rows", output)
        self.assertIn("[PEND]", output)
        self.assertIn("Your dataset contains header columns but 0 data rows.", output)

if __name__ == '__main__':
    unittest.main()
