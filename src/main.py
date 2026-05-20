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

def format_size(size_bytes):
    """Format size in bytes to a human-readable string."""
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

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

    missing_libs = []
    for label, name in libs.items():
        lib_version = get_lib_version(name)
        if lib_version:
            status = f"✅ {GREEN}{lib_version}{RESET}"
        else:
            status = f"❌ {RED}Not Found{RESET}"
            missing_libs.append(label)
        print(f"• {label:<15}: {status}")

    all_found = len(missing_libs) == 0

    data_dir_exists = os.path.isdir("data")
    data_count = 0
    total_size = 0
    if data_dir_exists:
        files = [f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))]
        data_count = len(files)
        total_size = sum(os.path.getsize(os.path.join("data", f)) for f in files)

    if data_dir_exists and data_count > 0:
        suffix = "file" if data_count == 1 else "files"
        size_str = format_size(total_size)
        data_status = f"✅ {GREEN}Found ({data_count} {suffix}, {size_str}){RESET}"
    elif data_dir_exists:
        data_status = f"⚠️ {YELLOW}Empty (0 files){RESET}"
    else:
        data_status = f"❌ {RED}Not Found{RESET}"
    print(f"• {'Data Source':<15}: {data_status}")

    if not all_found:
        lib_suffix = "library" if len(missing_libs) == 1 else "libraries"
        status_msg = f"❌ {RED}Incomplete ({len(missing_libs)} {lib_suffix} missing) - Please run: {BOLD}pip install -r requirements.txt{RESET}"
    elif not data_dir_exists or data_count == 0:
        status_msg = f"⚠️ {YELLOW}Pending - Data directory missing or empty{RESET}"
    else:
        status_msg = f"✅ {GREEN}Ready{RESET}"
    print(f"• {'Status':<15}: {status_msg}")

    print(f"\n🚀 Welcome! This tool is designed to help you extract insights from product data.")

    print(f"\n{GREEN}{BOLD}Analysis Roadmap:{RESET}")
    stages = [
        {"emoji": "📥", "label": "Data Ingestion", "desc": "Collect raw data from various sources."},
        {"emoji": "🧹", "label": "Data Cleaning", "desc": "Preprocess and handle missing values."},
        {"emoji": "📊", "label": "EDA", "desc": "Visualize and understand data distributions."},
        {"emoji": "⚙️", "label": "Feature Engineering", "desc": "Create new variables for modeling."},
        {"emoji": "🤖", "label": "Modeling", "desc": "Train and evaluate machine learning models."},
        {"emoji": "📈", "label": "Reporting & Insights", "desc": "Extract and communicate final results."},
    ]

    for i, stage in enumerate(stages, 1):
        if i == 1:
            if data_count > 0:
                status_tag = f"{GREEN}[DONE]{RESET}"
            elif all_found:
                status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
            else:
                status_tag = f"{YELLOW}[PEND]{RESET}"
        elif i == 2:
            if data_count > 0:
                status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
            else:
                status_tag = f"{YELLOW}[PEND]{RESET}"
        else:
            status_tag = f"{YELLOW}[PEND]{RESET}"

        print(f"{BOLD}{i}.{RESET} {stage['emoji']} {status_tag} {BOLD}{stage['label']:<20}:{RESET} {stage['desc']}")

    if not all_found:
        lib_suffix = "library" if len(missing_libs) == 1 else "libraries"
        tip_text = f"{len(missing_libs)} {lib_suffix} missing? Run the {BOLD}pip install -r requirements.txt{RESET} command."
    elif not data_dir_exists:
        tip_text = f"No data directory found? Run {BOLD}mkdir data{RESET} to create one."
    elif data_count == 0:
        tip_text = f"Data directory is empty? Add some product datasets to the {BOLD}data/{RESET} folder."
    else:
        tip_text = f"Ready to start? Head over to the {BOLD}Data Cleaning{RESET} stage to prepare your dataset!"

    print(f"\n💡 {CYAN}{BOLD}Tip:{RESET} {tip_text}")
    print(f"   Use {BOLD}--help{RESET} or refer to README.md for detailed documentation.")
    print(f"{BLUE}──────────────────────────────────────────{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted. Exiting gracefully...")
        sys.exit(0)
