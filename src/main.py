import argparse
import sys
import platform
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

    status_msg = f"✅ {GREEN}Ready{RESET}" if all_found else f"❌ {RED}Incomplete - Please run: {BOLD}pip install -r requirements.txt{RESET}"
    print(f"• {'Status':<15}: {status_msg}")

    print(f"\n🚀 Welcome! This tool is designed to help you extract insights from product data.")

    print(f"\n{GREEN}{BOLD}Analysis Roadmap:{RESET}")
    print(f"1. 📥 {BOLD}{'Data Ingestion':<20}:{RESET} Collect raw data from various sources.")
    print(f"2. 🧹 {BOLD}{'Data Cleaning':<20}:{RESET} Preprocess and handle missing values.")
    print(f"3. 📊 {BOLD}{'EDA':<20}:{RESET} Visualize and understand data distributions.")
    print(f"4. ⚙️ {BOLD}{'Feature Engineering':<20}:{RESET} Create new variables for modeling.")
    print(f"5. 🤖 {BOLD}{'Modeling':<20}:{RESET} Train and evaluate machine learning models.")
    print(f"6. 📈 {BOLD}{'Reporting':<20}:{RESET} Extract and communicate final results.")

    if all_found:
        tip_text = f"Ready to start? Check the {BOLD}Roadmap{RESET} above and run your first analysis!"
    else:
        tip_text = f"Dependencies missing? Run the {BOLD}pip install{RESET} command in the Status section above."

    print(f"\n💡 {CYAN}{BOLD}Tip:{RESET} {tip_text}")
    print(f"   Use {BOLD}--help{RESET} or refer to README.md for detailed documentation.")
    print(f"{BLUE}──────────────────────────────────────────{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted. Exiting gracefully...")
        sys.exit(0)
