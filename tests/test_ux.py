import unittest
from unittest.mock import patch
import sys
import io
import os
import shutil
from src.main import main

class TestUXImprovements(unittest.TestCase):
    def setUp(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        with open("data/test.csv", "w") as f:
            f.write("test")
        with open("data/test.json", "w") as f:
            f.write("{}")

    def tearDown(self):
        if os.path.exists("data"):
            shutil.rmtree("data")

    @patch('src.main.get_lib_version')
    @patch('sys.argv', ['src/main.py'])
    def test_ux_elements_with_data_and_libs(self, mock_get_version):
        mock_get_version.return_value = "1.2.3"
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            main()
            output = captured_output.getvalue()
            # Verify file type breakdown
            self.assertIn("1 CSV", output)
            self.assertIn("1 JSON", output)
            # Verify [DONE] status for Stage 1
            self.assertIn("[DONE]", output)
            # Verify [NEXT] status and indicator for Stage 2
            self.assertIn("[NEXT]", output)
            self.assertIn("◀ current", output)
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
