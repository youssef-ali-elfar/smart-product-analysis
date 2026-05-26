import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import os
from src.main import main

class TestUX(unittest.TestCase):
    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_roadmap_and_data_source_ux(self, mock_mtime, mock_size, mock_isfile, mock_listdir, mock_isdir, mock_get_lib):
        # Setup: All libs found, some data files present
        mock_get_lib.return_value = "1.2.3"
        mock_isdir.return_value = True
        mock_listdir.return_value = ['products.csv', 'sales.json', 'meta.txt']
        mock_isfile.return_value = True
        mock_size.return_value = 1024
        mock_mtime.return_value = 1622000000 # Some old timestamp

        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        # Check for file type breakdown
        self.assertIn("[1 CSV, 1 JSON, 1 TXT]", output)

        # Check for colorized labels and current indicator
        # [DONE] is GREEN (\033[92m)
        # [NEXT] is CYAN (\033[96m)
        self.assertIn("\033[92mData Ingestion", output)
        self.assertIn("\033[96mData Cleaning", output)
        self.assertIn("◀ current", output)

    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    def test_pending_state_ux(self, mock_isdir, mock_get_lib):
        # Setup: Libs missing, no data
        mock_get_lib.return_value = None
        mock_isdir.return_value = False

        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            main()
        except SystemExit:
            pass
        finally:
            sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        # Check that Stage 1 is [PEND]
        self.assertIn("[PEND]", output)
        self.assertIn("Data Ingestion", output)
        self.assertNotIn("◀ current", output)

if __name__ == "__main__":
    unittest.main()
