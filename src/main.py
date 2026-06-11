import argparse
import sys
import platform
import os
from datetime import datetime
from collections import Counter
import time

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
    # Ensure clean UX by removing unnecessary zeros
    return f"{s:g} {size_name[i]}"

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

    # 1. Environment & Data Checks (Proactive)
    libs = {
        "Pandas": "pandas",
        "NumPy": "numpy",
        "Matplotlib": "matplotlib",
        "Seaborn": "seaborn",
        "Scikit-Learn": "sklearn",
        "Jupyter": "jupyter"
    }

    lib_status_list = []
    missing_libs = []
    for label, name in libs.items():
        lib_version = get_lib_version(name)
        if lib_version:
            lib_status_list.append((label, f"✅ {GREEN}{lib_version}{RESET}"))
        else:
            lib_status_list.append((label, f"❌ {RED}{BOLD}Not Found{RESET}"))
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

    # Determine Badge & Status
    if not all_found:
        badge = "[INC]"
        badge_color = RED
    elif not data_dir_exists or data_count == 0:
        badge = "[PEND]"
        badge_color = YELLOW
    else:
        badge = "[READY]"
        badge_color = GREEN

    # 2. Header
    badge_padding = " " * (14 - len(badge) - len(version))
    print(f"{BLUE}┌────────────────────────────────────────┐{RESET}")
    print(f"{BLUE}│ {BOLD}Smart Product Analysis{RESET} v{version}{badge_padding}{BOLD}{badge_color}{badge}{RESET} {BLUE}│{RESET}")
    print(f"{BLUE}└────────────────────────────────────────┘{RESET}")

    # 3. System Status
    print(f"\n{CYAN}{BOLD}System Status:{RESET}")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"• {'Session Start':<15}: {now}")
    print(f"• {'System':<15}: {platform.system()} ({platform.machine()})")
    print(f"• {'Python':<15}: {platform.python_version()}")
    env_type = f"{GREEN}{BOLD}Virtual Env{RESET}" if is_venv() else f"{YELLOW}{BOLD}Global{RESET}"
    print(f"• {'Environment':<15}: {env_type}")

    for label, status in lib_status_list:
        print(f"• {label:<15}: {status}")

    if data_dir_exists and data_count > 0:
        suffix = "file" if data_count == 1 else "files"
        size_str = format_size(total_size)
        is_very_fresh = (time.time() - freshest_time) < 3600
        fresh_color = GREEN if is_very_fresh else RESET
        freshness = f" - Updated {fresh_color}{get_relative_time(freshest_time)}{RESET}"
        data_status = f"✅ {GREEN}{BOLD}Found{RESET} ({data_count} {suffix}: {type_summary}, {size_str}){freshness}"
    elif data_dir_exists:
        data_status = f"⚠️ {YELLOW}{BOLD}Empty{RESET} (0 files)"
    else:
        data_status = f"❌ {RED}{BOLD}Not Found{RESET}"
    print(f"• {'Data Source':<15}: {data_status}")

    if not all_found:
        lib_suffix = "library" if len(missing_libs) == 1 else "libraries"
        status_msg = f"❌ {RED}{BOLD}Incomplete{RESET} ({len(missing_libs)} {lib_suffix} missing) - Please run: {BOLD}pip install -r requirements.txt{RESET}"
    elif not data_dir_exists or data_count == 0:
        status_msg = f"⚠️ {YELLOW}{BOLD}Pending{RESET} - Data directory missing or empty"
    else:
        status_msg = f"✅ {GREEN}{BOLD}Ready{RESET}"
    print(f"• {'Status':<15}: {status_msg}")

    print(f"\n🚀 Welcome! This tool is designed to help you extract insights from product data.")

    # 4. Analysis Roadmap
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
                status_tag = f"{GREEN}{BOLD}[DONE]{RESET}"
                stage_color = GREEN
            elif all_found:
                status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
                stage_color = CYAN
                is_current = True
            else:
                status_tag = f"{YELLOW}{BOLD}[PEND]{RESET}"
                stage_color = RESET
        elif i == 2:
            if data_count > 0 and all_found:
                status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
                stage_color = CYAN
                is_current = True
            else:
                status_tag = f"{YELLOW}{BOLD}[PEND]{RESET}"
                stage_color = RESET
        else:
            status_tag = f"{YELLOW}{BOLD}[PEND]{RESET}"
            stage_color = RESET

        current_indicator = f" {CYAN}◀ current{RESET}" if is_current else ""

        # Add vertical connector line
        prefix = f"{BOLD}{i}.{RESET}"
        if i < len(stages):
            print(f"{prefix} {stage['emoji']} {status_tag} {BOLD}{stage_color}{stage['label']:<20}:{RESET} {stage['desc']}{current_indicator}")
            print(f"   {BOLD}│{RESET}")
        else:
            print(f"{prefix} {stage['emoji']} {status_tag} {BOLD}{stage_color}{stage['label']:<20}:{RESET} {stage['desc']}{current_indicator}")

    # 5. Onboarding Tip
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
