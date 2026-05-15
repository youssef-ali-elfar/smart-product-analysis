import argparse
import sys
import platform
import os
from datetime import datetime

def get_lib_version(name):
    """Safely get the version of a library."""
    try:
        module = __import__(name)
        return getattr(module, "__version__", "Unknown")
    except ImportError:
        return None

def main():
    version = "1.0.0"
    parser = argparse.ArgumentParser(
        description="Smart Product Analysis - A tool for analyzing product data."
    )
    parser.add_argument(
        "--version", action="version", version=f"Smart Product Analysis {version}"
    )

    # Parse arguments
    parser.parse_args()

    # ANSI colors
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"{BLUE}┌────────────────────────────────────────┐{RESET}")
    print(f"{BLUE}│ {BOLD}Smart Product Analysis{RESET} v{version:<14} {BLUE}│{RESET}")
    print(f"{BLUE}└────────────────────────────────────────┘{RESET}")

    # System Status
    print(f"\n{CYAN}{BOLD}System Status:{RESET}")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"• {'Session Start':<15}: {now}")
    print(f"• {'System':<15}: {platform.system()} ({platform.machine()})")
    print(f"• {'Python':<15}: {platform.python_version()}")

    libs = {
        "Pandas": "pandas",
        "NumPy": "numpy",
        "Matplotlib": "matplotlib",
        "Seaborn": "seaborn",
        "Scikit-Learn": "sklearn",
        "Jupyter": "jupyter"
    }

    all_found = True
    for label, name in libs.items():
        lib_version = get_lib_version(name)
        if lib_version:
            status = f"✅ {GREEN}{lib_version}{RESET}"
        else:
            status = f"❌ {RED}Not Found{RESET}"
            all_found = False
        print(f"• {label:<15}: {status}")

    data_dir_exists = os.path.isdir("data")
    data_count = 0
    if data_dir_exists:
        data_count = len([f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))])

    if data_dir_exists and data_count > 0:
        data_status = f"✅ {GREEN}Found ({data_count} files){RESET}"
    elif data_dir_exists:
        data_status = f"⚠️ {YELLOW}Empty (0 files){RESET}"
    else:
        data_status = f"❌ {RED}Not Found{RESET}"
    print(f"• {'Data Source':<15}: {data_status}")

    if not all_found:
        status_msg = f"❌ {RED}Incomplete - Please run: {BOLD}pip install -r requirements.txt{RESET}"
    elif not data_dir_exists or data_count == 0:
        status_msg = f"⚠️ {YELLOW}Pending - Data directory missing or empty{RESET}"
    else:
        status_msg = f"✅ {GREEN}Ready{RESET}"
    print(f"• {'Status':<15}: {status_msg}")

    print(f"\n🚀 Welcome! This tool is designed to help you extract insights from product data.")

    print(f"\n{GREEN}{BOLD}Analysis Roadmap:{RESET}")
    print(f"{BOLD}1.{RESET} 📥 {BOLD}{'Data Ingestion':<20}:{RESET} Collect raw data from various sources.")
    print(f"{BOLD}2.{RESET} 🧹 {BOLD}{'Data Cleaning':<20}:{RESET} Preprocess and handle missing values.")
    print(f"{BOLD}3.{RESET} 📊 {BOLD}{'EDA':<20}:{RESET} Visualize and understand data distributions.")
    print(f"{BOLD}4.{RESET} ⚙️ {BOLD}{'Feature Engineering':<20}:{RESET} Create new variables for modeling.")
    print(f"{BOLD}5.{RESET} 🤖 {BOLD}{'Modeling':<20}:{RESET} Train and evaluate machine learning models.")
    print(f"{BOLD}6.{RESET} 📈 {BOLD}{'Reporting & Insights':<20}:{RESET} Extract and communicate final results.")

    if not all_found:
        tip_text = f"Dependencies missing? Run the {BOLD}pip install -r requirements.txt{RESET} command."
    elif not data_dir_exists:
        tip_text = f"No data directory found? Run {BOLD}mkdir data{RESET} to create one."
    elif data_count == 0:
        tip_text = f"Data directory is empty? Add some product datasets to the {BOLD}data/{RESET} folder."
    else:
        tip_text = f"Ready to start? Check the {BOLD}Roadmap{RESET} above and run your first analysis!"

    print(f"\n💡 {CYAN}{BOLD}Tip:{RESET} {tip_text}")
    print(f"   Use {BOLD}--help{RESET} or refer to README.md for detailed documentation.")
    print(f"{BLUE}──────────────────────────────────────────{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted. Exiting gracefully...")
        sys.exit(0)
