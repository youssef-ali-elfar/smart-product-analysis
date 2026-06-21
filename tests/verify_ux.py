import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import os
from src.main import main

class TestUX(unittest.TestCase):
    @patch('sys.argv', ['src/main.py'])
    @patch('src.main.get_lib_version')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('os.path.getmtime')
    def test_output_scenarios(self, mock_getmtime, mock_getsize, mock_isfile, mock_listdir, mock_isdir, mock_get_lib_version):
        scenarios = [
            {
                "name": "Missing Libraries and Missing Data",
                "libs": {lib: None for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": False,
                "data_files": []
            },
            {
                "name": "All Libraries Found but Empty Data",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": []
            },
            {
                "name": "All Libraries and Data Found",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["products.csv", "metadata.json", "styles.css"],
                "file_times": [1716843600, 1716843600, 1716843600] # Mocked times
            },
            {
                "name": "Pluralized Data Types",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["data1.csv", "data2.csv", "info.json"],
                "file_times": [1716843600, 1716843600, 1716843600]
            },
            {
                "name": "Single Data Type",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["data1.csv"],
                "file_times": [1716843600]
            }
        ]

        import time
        current_time = time.time()

        for scenario in scenarios:
            print(f"\n{'='*20} Scenario: {scenario['name']} {'='*20}")

            # Setup mocks
            mock_get_lib_version.side_effect = lambda name: scenario['libs'].get(name)
            mock_isdir.return_value = scenario['data_dir_exists']
            mock_listdir.return_value = scenario['data_files']
            mock_isfile.return_value = True
            mock_getsize.return_value = 1024

            if "file_times" in scenario:
                # Make the first file very fresh (just now)
                mock_getmtime.side_effect = [current_time - 10] + [current_time - 7200] * (len(scenario['data_files']) - 1)
            else:
                mock_getmtime.side_effect = None
                mock_getmtime.return_value = current_time - 100000

            captured_output = io.StringIO()
            sys.stdout = captured_output
            try:
                main()
                output = captured_output.getvalue()
                sys.stdout = sys.__stdout__
                print(output)
            except Exception as e:
                sys.stdout = sys.__stdout__
                print(f"Error in scenario {scenario['name']}: {e}")
            finally:
                sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
