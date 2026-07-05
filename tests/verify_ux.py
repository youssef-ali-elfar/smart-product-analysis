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
    @patch('src.main.supports_color')
    @patch('os.path.getmtime')
    def test_output_scenarios(self, mock_getmtime, mock_supports_color, mock_getsize, mock_isfile, mock_listdir, mock_isdir, mock_get_lib_version):
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
                "name": "Multiple Files Pluralization",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["data1.csv", "data2.csv", "info.json"],
                "file_times": [1716843600, 1716843600, 1716843600]
            },
            {
                "name": "Many File Types Capping",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["a.csv", "b.json", "c.txt", "d.parquet", "e.xls"],
                "file_times": [1716843600] * 5
            },
            {
                "name": "One Missing Library Tip",
                "libs": {lib: "1.2.3" for lib in ["numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["products.csv"]
            },
            {
                "name": "Two Missing Libraries Tip",
                "libs": {lib: "1.2.3" for lib in ["matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["products.csv"]
            },
            {
                "name": "NO_COLOR Support",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["products.csv"],
                "env": {"NO_COLOR": "1"}
            }
        ]

        import time
        current_time = time.time()

        for scenario in scenarios:
            print(f"\n{'='*20} Scenario: {scenario['name']} {'='*20}")

            # Setup mocks
            if "env" in scenario:
                patcher = patch.dict(os.environ, scenario["env"])
                patcher.start()
                mock_supports_color.return_value = "NO_COLOR" not in scenario["env"]
            else:
                mock_supports_color.return_value = True

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

                if scenario['data_dir_exists'] and scenario['data_files']:
                    self.assertIn("Composition", output)
                    self.assertIn("Freshness", output)

                if scenario['name'] == "Many File Types Capping":
                    self.assertIn("2 others", output)
                    self.assertIn("Latest", output)
                    # Extension should be bolded: \033[1mCSV\033[0m
                    self.assertIn("\033[1mCSV\033[0m", output)

                if scenario['name'] == "NO_COLOR Support":
                    self.assertNotIn("\033[", output)

            except Exception as e:
                sys.stdout = sys.__stdout__
                print(f"Error in scenario {scenario['name']}: {e}")
            finally:
                sys.stdout = sys.__stdout__
                if "env" in scenario:
                    patcher.stop()

if __name__ == '__main__':
    unittest.main()
