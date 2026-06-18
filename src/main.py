import argparse
import sys
import platform
import os
import math
import time
from collections import Counter
from datetime import datetime

def is_venv():
    """Detect if the script is running in a virtual environment."""
    return (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )

def get_relative_time(timestamp):
    """Format a timestamp into a human-readable relative time."""
    diff = datetime.now() - datetime.fromtimestamp(timestamp)
    seconds = diff.total_seconds()
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes}m ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours}h ago"
    else:
        days = int(seconds // 86400)
        return f"{days}d ago"

def get_lib_version(name):
    """Safely get the version of a library."""
    try:
        module = __import__(name)
        return getattr(module, "__version__", "Detected")
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

    # Environment and Dependency Checks
    libs = {
        "Pandas": "pandas",
        "NumPy": "numpy",
        "Matplotlib": "matplotlib",
        "Seaborn": "seaborn",
        "Scikit-Learn": "sklearn",
        "Jupyter": "jupyter"
    }

    missing_libs = []
    lib_results = {}
    for label, name in libs.items():
        v = get_lib_version(name)
        lib_results[label] = v
        if not v:
            missing_libs.append(label)

    all_found = len(missing_libs) == 0
    data_dir_exists = os.path.isdir("data")
    data_count = 0
    total_size = 0
    freshest_time = 0
    type_summary = ""

    if data_dir_exists:
        files = [f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))]
        data_count = len(files)
        file_types = []
        for f in files:
            path = os.path.join("data", f)
            total_size += os.path.getsize(path)
            freshest_time = max(freshest_time, os.path.getmtime(path))
            ext = os.path.splitext(f)[1][1:].upper() or "OTHER"
            file_types.append(ext)
        type_counts = Counter(file_types)
        type_summary = ", ".join([f"{count} {t}" for t, count in type_counts.items()])

    # Determine Status Logic
    if not all_found:
        badge_text = "INC"
        badge_color = RED
        lib_suffix = "library" if len(missing_libs) == 1 else "libraries"
        status_msg = f"❌ {BOLD}{RED}Incomplete{RESET} ({len(missing_libs)} {lib_suffix} missing) - Please run: {BOLD}pip install -r requirements.txt{RESET}"
    elif not data_dir_exists or data_count == 0:
        badge_text = "PEND"
        badge_color = YELLOW
        status_msg = f"⚠️ {BOLD}{YELLOW}Pending{RESET} - Data directory missing or empty"
    else:
        badge_text = "READY"
        badge_color = GREEN
        status_msg = f"✅ {BOLD}{GREEN}Ready{RESET}"

    badge = f"{badge_color}[{badge_text}]{RESET}"

    # Header - formula: 12 - len(badge_text) - len(version)
    # The box is 42 chars wide, internal content (including spaces) must be 40.
    # "Smart Product Analysis" (22) + " v" (2) + version + padding + badge + 2 spaces = 40
    # 24 + version + padding + (badge_text + 2) + 2 = 40
    # 28 + version + padding + badge_text = 40
    # padding = 12 - len(version) - len(badge_text)
    padding_count = 12 - len(version) - len(badge_text)
    padding = " " * padding_count

    print(f"{BLUE}┌────────────────────────────────────────┐{RESET}")
    print(f"{BLUE}│ {BOLD}Smart Product Analysis{RESET} v{version}{padding}{badge} {BLUE}│{RESET}")
    print(f"{BLUE}└────────────────────────────────────────┘{RESET}")

    # System Status
    print(f"\n{CYAN}{BOLD}System Status:{RESET}")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"• {'Session Start':<15}: {now}")
    print(f"• {'System':<15}: {platform.system()} ({platform.machine()})")
    print(f"• {'Python':<15}: {platform.python_version()}")
    env_type = f"{BOLD}{GREEN}Virtual Env{RESET}" if is_venv() else f"{BOLD}{YELLOW}Global{RESET}"
    print(f"• {'Environment':<15}: {env_type}")

    for label, v in lib_results.items():
        if v:
            status = f"✅ {GREEN}{v}{RESET}"
        else:
            status = f"❌ {RED}Not Found{RESET}"
        print(f"• {label:<15}: {status}")

    if data_dir_exists and data_count > 0:
        suffix = "file" if data_count == 1 else "files"
        size_str = format_size(total_size)
        is_very_fresh = (time.time() - freshest_time) < 3600
        fresh_color = GREEN if is_very_fresh else RESET
        freshness = f" - Updated {fresh_color}{get_relative_time(freshest_time)}{RESET}"
        data_status = f"✅ {GREEN}Found ({data_count} {suffix}: {type_summary}, {size_str}){RESET}{freshness}"
    elif data_dir_exists:
        data_status = f"⚠️ {BOLD}{YELLOW}Empty (0 files){RESET}"
    else:
        data_status = f"❌ {BOLD}{RED}Not Found{RESET}"
    print(f"• {'Data Source':<15}: {data_status}")

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
        is_current = False
        if i == 1:
            if data_count > 0:
                status_tag = f"{BOLD}{GREEN}[DONE]{RESET}"
                stage_color = GREEN
            elif all_found:
                status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
                stage_color = CYAN
                is_current = True
            else:
                status_tag = f"{BOLD}{YELLOW}[PEND]{RESET}"
                stage_color = RESET
        elif i == 2:
            if data_count > 0 and all_found:
                status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
                stage_color = CYAN
                is_current = True
            else:
                status_tag = f"{BOLD}{YELLOW}[PEND]{RESET}"
                stage_color = RESET
        else:
            status_tag = f"{BOLD}{YELLOW}[PEND]{RESET}"
            stage_color = RESET

        if i > 1:
            print(f"   {BLUE}│{RESET}")
        current_indicator = f" {CYAN}◀ current{RESET}" if is_current else ""
        print(f"{BOLD}{i}.{RESET} {stage['emoji']} {status_tag} {BOLD}{stage_color}{stage['label']:<20}:{RESET} {stage['desc']}{current_indicator}")

    if not all_found:
        lib_suffix = "library" if len(missing_libs) == 1 else "libraries"
        tip_text = f"{len(missing_libs)} {lib_suffix} missing? Run the {BOLD}pip install -r requirements.txt{RESET} command to set up your environment."
    elif not data_dir_exists:
        tip_text = f"Almost there! Run {BOLD}mkdir data{RESET} and add your product datasets to get started."
    elif data_count == 0:
        tip_text = f"Data folder is ready but empty. Add some CSV or JSON product datasets to {BOLD}data/{RESET} to begin."
    else:
        tip_text = f"✨ {BOLD}Everything is set!{RESET} Head over to the {BOLD}Data Cleaning{RESET} stage to prepare your dataset!"

    print(f"\n💡 {CYAN}{BOLD}Tip:{RESET} {tip_text}")
    print(f"   Use {BOLD}--help{RESET} or refer to README.md for detailed documentation.")
    print(f"{BLUE}──────────────────────────────────────────{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted. Exiting gracefully...")
        sys.exit(0)
