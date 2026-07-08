import argparse
import sys
import platform
import os
import math
import time
from datetime import datetime
from collections import Counter

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
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = size_bytes / p
    return f"{s:g} {size_name[i]}"

def natural_join(items):
    """Format a list of strings into a grammatically correct natural language string."""
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"

def supports_color():
    """Check if the terminal supports color."""
    if "NO_COLOR" in os.environ:
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    return True

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
    use_color = supports_color()
    BLUE = "\033[94m" if use_color else ""
    GREEN = "\033[92m" if use_color else ""
    RED = "\033[91m" if use_color else ""
    YELLOW = "\033[93m" if use_color else ""
    CYAN = "\033[96m" if use_color else ""
    BOLD = "\033[1m" if use_color else ""
    RESET = "\033[0m" if use_color else ""

    # Consolidated Checks
    libs = {
        "Pandas": {"pkg": "pandas", "purpose": "Data manipulation"},
        "NumPy": {"pkg": "numpy", "purpose": "Numerical computing"},
        "Matplotlib": {"pkg": "matplotlib", "purpose": "Static visualizations"},
        "Seaborn": {"pkg": "seaborn", "purpose": "Statistical data visualization"},
        "Scikit-Learn": {"pkg": "sklearn", "purpose": "Machine learning algorithms"},
        "Jupyter": {"pkg": "jupyter", "purpose": "Interactive notebooks"}
    }

    lib_results = {}
    missing_libs = []
    for label, info in libs.items():
        lib_version = get_lib_version(info["pkg"])
        lib_results[label] = lib_version
        if not lib_version:
            missing_libs.append(label)

    all_found = len(missing_libs) == 0

    data_dir_exists = os.path.isdir("data")
    data_count = 0
    total_size = 0
    freshest_time = 0
    type_summary = ""
    if data_dir_exists:
        files = sorted([f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))])
        data_count = len(files)
        file_types = []
        latest_file = ""
        for f in files:
            path = os.path.join("data", f)
            mtime = os.path.getmtime(path)
            total_size += os.path.getsize(path)
            if mtime > freshest_time:
                freshest_time = mtime
                latest_file = f
            ext = os.path.splitext(f)[1][1:].upper() or "OTHER"
            file_types.append(ext)
        type_counts = Counter(file_types)
        common_types = type_counts.most_common(3)
        type_items = [f"{count} {BOLD}{t}{RESET} {'file' if count == 1 else 'files'}" for t, count in common_types]

        # Calculate total files in remaining types
        if len(type_counts) > 3:
            total_others = sum(count for t, count in type_counts.most_common()[3:])
            type_items.append(f"{total_others} others")

        type_summary = natural_join(type_items)

    # Determine Status and Badge
    if not all_found:
        badge_text = f"[INC:{len(missing_libs)}]"
        badge_color = RED
    elif not data_dir_exists or data_count == 0:
        badge_text = "[PEND]"
        badge_color = YELLOW
    else:
        badge_text = "[READY]"
        badge_color = GREEN

    # Print Header
    padding_count = 13 - len(version) - len(badge_text)
    padding = " " * padding_count
    print(f"{BLUE}┌────────────────────────────────────────┐{RESET}")
    print(f"{BLUE}│ {BOLD}Smart Product Analysis{RESET} v{version} {padding}{badge_color}{BOLD}{badge_text}{RESET} {BLUE}│{RESET}")
    print(f"{BLUE}└────────────────────────────────────────┘{RESET}")

    # System Status
    print(f"\n{CYAN}{BOLD}System Status:{RESET}")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"• {'Session Start':<15}: 🕒 {now}")
    os_name = platform.system()
    os_icon = "🐧 " if os_name == "Linux" else "🍎 " if os_name == "Darwin" else "🪟 " if os_name == "Windows" else ""
    print(f"• {'System':<15}: {os_icon}{os_name} ({platform.machine()})")
    print(f"• {'Python':<15}: {platform.python_version()}")
    env_type = f"📦 {BOLD}{GREEN}Virtual Env{RESET}" if is_venv() else f"🌐 {BOLD}{YELLOW}Global{RESET}"
    print(f"• {'Environment':<15}: {env_type}")

    print(f"  {BOLD}Dependencies:{RESET}")
    for label, lib_version in lib_results.items():
        if lib_version:
            status = f"✅ {BOLD}{GREEN}{lib_version}{RESET}"
        else:
            purpose = libs[label]["purpose"]
            status = f"❌ {BOLD}{RED}Not Found{RESET} ({purpose})"
        print(f"  - {label:<13}: {status}")

    if data_dir_exists and data_count > 0:
        suffix = "file" if data_count == 1 else "files"
        size_str = format_size(total_size)
        time_diff = time.time() - freshest_time
        is_very_fresh = time_diff < 86400
        is_stale = time_diff > 604800
        fresh_color = GREEN if is_very_fresh else RESET
        warning_str = f" {BOLD}{YELLOW}(Stale?){RESET}" if is_stale else ""
        freshness = f"Updated {BOLD}{fresh_color}{get_relative_time(freshest_time)}{RESET}{warning_str}"
        print(f"• {'Data Source':<15}: ✅ {BOLD}{GREEN}Found{RESET} ({data_count} {suffix}, {size_str})")
        if 1 <= data_count <= 3:
            file_list = natural_join([f"{BOLD}{f}{RESET}" for f in files])
            print(f"  - {'Files':<13}: {file_list}")
        elif data_count > 3:
            print(f"  - {'Latest':<13}: {BOLD}{latest_file}{RESET}")
        print(f"  - {'Composition':<13}: {type_summary}")
        print(f"  - {'Freshness':<13}: {freshness}")
    elif data_dir_exists:
        data_status = f"⚠️ {BOLD}{YELLOW}Empty (0 files){RESET}"
        print(f"• {'Data Source':<15}: {data_status}")
    else:
        data_status = f"❌ {BOLD}{RED}Not Found{RESET}"
        print(f"• {'Data Source':<15}: {data_status}")

    if not all_found:
        lib_suffix = "library" if len(missing_libs) == 1 else "libraries"
        status_msg = f"❌ {BOLD}{RED}Incomplete{RESET} ({len(missing_libs)} {lib_suffix} missing) - Please run: {BOLD}pip install -r requirements.txt{RESET}"
    elif not data_dir_exists or data_count == 0:
        status_msg = f"⚠️ {BOLD}{YELLOW}Pending{RESET} - Data directory missing or empty"
    else:
        status_msg = f"✅ {BOLD}{GREEN}Ready{RESET}"
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

    prev_stage_done = False
    for i, stage in enumerate(stages, 1):
        if i > 1:
            connector_color = GREEN if prev_stage_done else BLUE
            print(f"   {connector_color}│{RESET}")
        is_current = False
        this_stage_done = False
        if i == 1:
            if data_count > 0:
                status_tag = f"{BOLD}{GREEN}[DONE]{RESET}"
                stage_color = GREEN
                this_stage_done = True
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

        current_indicator = f" {CYAN}◀ current{RESET}" if is_current else ""
        print(f"{BOLD}{i}.{RESET} {stage['emoji']} {status_tag} {BOLD}{stage_color}{stage['label']:<20}:{RESET} {stage['desc']}{current_indicator}")
        prev_stage_done = this_stage_done

    is_virtual = is_venv()
    if not all_found:
        if len(missing_libs) <= 2:
            missing_list = natural_join([f"{BOLD}{m}{RESET}" for m in missing_libs])
            tip_text = f"Missing {missing_list}? Run {BOLD}pip install -r requirements.txt{RESET} to complete your setup."
        else:
            tip_text = f"{len(missing_libs)} libraries missing? Run the {BOLD}pip install -r requirements.txt{RESET} command to set up your environment."
    elif not data_dir_exists:
        tip_text = f"Almost there! Run {BOLD}mkdir data{RESET} and add your product datasets to get started."
        if not is_virtual:
            tip_text += f" (Tip: Use a {BOLD}Virtual Env{RESET} for better management!)"
    elif data_count == 0:
        tip_text = f"Data folder is ready but empty. Add some CSV or JSON product datasets to {BOLD}data/{RESET} to begin."
        if not is_virtual:
            tip_text += f" (Tip: Use a {BOLD}Virtual Env{RESET} for better management!)"
    elif not is_virtual:
        tip_text = f"Consider using a {BOLD}Virtual Environment{RESET} for better dependency management. Run {BOLD}python -m venv venv{RESET} to create one!"
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
