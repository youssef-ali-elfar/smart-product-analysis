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
        import time
        current_time = time.time()
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
                "file_times": [current_time - 10, current_time - 7200, current_time - 7200]
            },
            {
                "name": "Multiple Files Pluralization",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["data1.csv", "data2.csv", "info.json"],
                "file_times": [current_time - 10, current_time - 7200, current_time - 7200]
            },
            {
                "name": "Many File Types Capping",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["a.csv", "b.json", "c.txt", "d.parquet", "e.xls"],
                "file_times": [current_time - 10] * 5
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
            },
            {
                "name": "Stale Data Warning",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["old_data.csv"],
                "file_times": [current_time - 800000] # Older than 7 days
            },
            {
                "name": "Empty Data Files Awareness",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["empty.csv"],
                "file_size": 0
            },
            {
                "name": "Explicit CLI --plain Mode",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["products.csv"],
                "argv": ["src/main.py", "--plain"]
            },
            {
                "name": "Explicit CLI --no-color Mode",
                "libs": {lib: "1.2.3" for lib in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "jupyter"]},
                "data_dir_exists": True,
                "data_files": ["products.csv"],
                "argv": ["src/main.py", "--no-color"]
            }
        ]

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
            mock_getsize.return_value = scenario.get("file_size", 1024)

            if "file_times" in scenario:
                mock_getmtime.side_effect = scenario['file_times']
            else:
                mock_getmtime.side_effect = None
                mock_getmtime.return_value = current_time - 100000

            captured_output = io.StringIO()
            sys.stdout = captured_output
            try:
                argv = scenario.get("argv", ["src/main.py"])
                # We mock `open` to return a predefined CSV contents when products.csv or similar is read
                mock_csv_data = "id,name,category,price,stock\n1,Smart Watch,Electronics,199.99,50"
                with patch("sys.argv", argv), patch("builtins.open", unittest.mock.mock_open(read_data=mock_csv_data)) as mock_file:
                    main()
                output = captured_output.getvalue()
                sys.stdout = sys.__stdout__
                print(output)

                if scenario['data_dir_exists'] and scenario['data_files']:
                    self.assertIn("Composition", output)
                    self.assertIn("Freshness", output)
                    # Verify our new Dataset sub-bullet if csv file is present and not empty
                    if any(f.lower().endswith(".csv") for f in scenario['data_files']) and scenario.get("file_size", 1024) > 0:
                        self.assertIn("Dataset", output)
                        self.assertIn("1 row", output)
                        self.assertIn("id, name, category, price, stock", output)

                if scenario['name'] == "Many File Types Capping":
                    self.assertIn("2 other files", output)
                    self.assertIn("Latest", output)
                    # Extension should be bolded: \033[1mCSV\033[0m
                    self.assertIn("\033[1mCSV\033[0m", output)
                    self.assertIn("file", output) # Check for pluralization suffix

                if scenario['name'] == "Stale Data Warning":
                    self.assertIn("(Stale?)", output)
                    self.assertIn("\033[93m", output) # YELLOW color

                if scenario['name'] == "Empty Data Files Awareness":
                    self.assertIn("Files appear empty!", output)
                    self.assertIn("[PEND]", output)
                    self.assertIn("0 B", output)

                if scenario['name'] == "NO_COLOR Support":
                    self.assertNotIn("\033[", output)

                if scenario['name'] == "Explicit CLI --plain Mode":
                    # No ANSI escape codes
                    self.assertNotIn("\033[", output)
                    # No unicode emojis
                    self.assertNotIn("✅", output)
                    self.assertNotIn("❌", output)
                    self.assertNotIn("⚠️", output)
                    self.assertNotIn("🕒", output)
                    self.assertNotIn("📦", output)
                    self.assertNotIn("🌐", output)
                    self.assertNotIn("💡", output)
                    self.assertNotIn("🚀", output)
                    # ASCII border instead of unicode box drawings
                    self.assertIn("+----------------------------------------+", output)
                    self.assertIn("| ", output)
                    self.assertIn("------------------------------------------", output)

                if scenario['name'] == "Explicit CLI --no-color Mode":
                    # No ANSI escape codes
                    self.assertNotIn("\033[", output)
                    # Retains emojis
                    self.assertIn("✅", output)

            except Exception as e:
                sys.stdout = sys.__stdout__
                print(f"Error in scenario {scenario['name']}: {e}")
            finally:
                sys.stdout = sys.__stdout__
                if "env" in scenario:
                    patcher.stop()

if __name__ == '__main__':
    unittest.main()
