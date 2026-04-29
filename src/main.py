import argparse
import sys
import platform
from datetime import datetime

def get_lib_version(name):
    """Safely retrieves the version of a library."""
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
    print(f"{BLUE}│ {BOLD}Smart Product Analysis{RESET} v{version:<11} {BLUE}│{RESET}")
    print(f"{BLUE}└────────────────────────────────────────┘{RESET}")

    # System Status
    session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    libraries = {
        "Python": platform.python_version(),
        "Pandas": get_lib_version("pandas"),
        "NumPy": get_lib_version("numpy"),
        "Matplotlib": get_lib_version("matplotlib"),
        "Seaborn": get_lib_version("seaborn"),
        "Scikit-Learn": get_lib_version("sklearn"),
    }

    print(f"\n{CYAN}{BOLD}System Status:{RESET}")
    print(f"{'Session':<15}: {session_time}")

    for label, lib_version in libraries.items():
        if lib_version:
            status_text = lib_version
        else:
            status_text = f"{RED}Not Found{RESET}"
        print(f"{label:<15}: {status_text}")

    print(f"{'Status':<15}: {GREEN}Ready{RESET}")

    print(f"\nWelcome! This tool is designed to help you extract insights from product data.")

    print(f"\n{GREEN}{BOLD}Analysis Roadmap:{RESET}")
    print(f"1. 📥 {BOLD}Data Ingestion:{RESET} Collect raw data from various sources.")
    print(f"2. 🧹 {BOLD}Data Cleaning:{RESET} Preprocess and handle missing values.")
    print(f"3. 📊 {BOLD}EDA:{RESET} Visualize and understand data distributions.")
    print(f"4. ⚙️ {BOLD}Feature Engineering:{RESET} Create new variables for modeling.")
    print(f"5. 🤖 {BOLD}Modeling:{RESET} Train and evaluate machine learning models.")
    print(f"6. 📈 {BOLD}Reporting:{RESET} Extract and communicate final results.")

    print(f"\n{CYAN}{BOLD}Tip:{RESET} Use {BOLD}--help{RESET} or refer to README.md for detailed documentation.")
    print(f"{BLUE}──────────────────────────────────────────{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted. Exiting gracefully...")
        sys.exit(0)
