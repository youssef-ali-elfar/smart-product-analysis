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
    epilog_text = """examples:
  python src/main.py            Run standard workspace analysis & check dependencies
  python src/main.py --init     Initialize data/ directory and sample products dataset
  python src/main.py --plain    Run status report in screen-reader friendly plain text mode
  python src/main.py --no-color Suppress ANSI color codes while keeping icons
"""
    parser = argparse.ArgumentParser(
        description="Smart Product Analysis - A tool for analyzing product data.",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--version", action="version", version=f"Smart Product Analysis {version}"
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable ANSI color output"
    )
    parser.add_argument(
        "--plain", action="store_true", help="Plain text mode (no colors, no emojis, no box drawing)"
    )
    parser.add_argument(
        "-i", "--init", action="store_true", help="Initialize data/ directory and populate it with a sample products.csv file"
    )

    # Parse arguments
    args = parser.parse_args()

    # ANSI colors
    use_color = supports_color() and not args.no_color and not args.plain
    BLUE = "\033[94m" if use_color else ""
    GREEN = "\033[92m" if use_color else ""
    RED = "\033[91m" if use_color else ""
    YELLOW = "\033[93m" if use_color else ""
    CYAN = "\033[96m" if use_color else ""
    BOLD = "\033[1m" if use_color else ""
    RESET = "\033[0m" if use_color else ""

    # Emoji / Special Character Constants
    EMOJI_OK = "" if args.plain else "✅ "
    EMOJI_ERR = "" if args.plain else "❌ "
    EMOJI_WARN = "" if args.plain else "⚠️ "
    EMOJI_TIME = "" if args.plain else "🕒 "
    EMOJI_VENV = "" if args.plain else "📦 "
    EMOJI_GLOBAL = "" if args.plain else "🌐 "
    EMOJI_TIP = "" if args.plain else "💡 "
    EMOJI_ROCKET = "" if args.plain else "🚀 "
    EMOJI_SPARKLES = "" if args.plain else "✨ "

    # Bullet and Separator Constants
    BULLET = "-" if args.plain else "•"
    SEP = "|" if args.plain else "•"

    if args.init:
        csv_path = os.path.join("data", "products.csv")
        if os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0:
            if hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
                while True:
                    try:
                        response = input(f"{EMOJI_WARN}{BOLD}{YELLOW}Warning:{RESET} {BOLD}{csv_path}{RESET} already exists and contains data. Overwrite? [y/N/help]: ").strip().lower()
                        if response in ("?", "h", "help"):
                            print(f"\n{EMOJI_TIP}{CYAN}{BOLD}Help - Overwriting Data:{RESET}")
                            print(f"  An existing products dataset already resides in {BOLD}{csv_path}{RESET}.")
                            print("  - If you overwrite it, the file will be replaced with clean sample mock data (5 products).")
                            print("  - If you abort, your current data and custom changes will remain intact.\n")
                            continue
                        elif response in ("y", "yes"):
                            break
                        elif response in ("n", "no", ""):
                            print(f"\n{BOLD}Initialization aborted.{RESET}\n")
                            return
                        else:
                            print(f"\n{EMOJI_WARN}{BOLD}{YELLOW}Unrecognized option:{RESET} {BOLD}'{response}'{RESET}. Please enter y, yes, n, no, h, help, or press Enter to decline.\n")
                            continue
                    except (KeyboardInterrupt, EOFError):
                        print(f"\n\n👋 Initialization interrupted. Exiting gracefully...\n")
                        sys.exit(0)

        # Create data directory and populate sample file
        os.makedirs("data", exist_ok=True)
        sample_data = (
            "id,name,category,price,stock\n"
            "1,Smart Watch,Electronics,199.99,50\n"
            "2,Wireless Earbuds,Electronics,79.99,120\n"
            "3,Running Shoes,Apparel,89.95,85\n"
            "4,Leather Wallet,Accessories,35.00,200\n"
            "5,Coffee Maker,Home,49.99,40\n"
        )
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write(sample_data)

        print(f"\n{EMOJI_SPARKLES}{BOLD}{GREEN}Initialization complete!{RESET}")
        print(f"{BULLET} Created {BOLD}data/{RESET} directory.")
        print(f"{BULLET} Populated {BOLD}data/products.csv{RESET} with sample product datasets.")
        print(f"{BULLET} Run {BOLD}python src/main.py{RESET} to view your updated workspace status!\n")
        return

    refreshed = False
    while True:
        # Borders and formatting constants
        if args.plain:
            border_top = "+----------------------------------------+"
            border_bottom = "+----------------------------------------+"
            border_mid_left = "| "
            border_mid_right = " |"
            connector_sym = "|"
            current_indicator_sym = "<- current"
            footer_line = "------------------------------------------"
        else:
            border_top = f"{BLUE}┌────────────────────────────────────────┐{RESET}"
            border_bottom = f"{BLUE}└────────────────────────────────────────┘{RESET}"
            border_mid_left = f"{BLUE}│ "
            border_mid_right = f" {BLUE}│{RESET}"
            connector_sym = "│"
            current_indicator_sym = "◀ current"
            footer_line = f"{BLUE}──────────────────────────────────────────{RESET}"

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
        missing_values_count = 0
        missing_val_cols = []
        if data_dir_exists:
            files = sorted([f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))])
            data_count = len(files)
            file_types = []
            latest_file = ""
            file_sizes = {}
            for f in files:
                path = os.path.join("data", f)
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    mtime = 0
                try:
                    size = os.path.getsize(path)
                except OSError:
                    size = 0
                file_sizes[f] = size
                total_size += size
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
                other_suffix = "file" if total_others == 1 else "files"
                type_items.append(f"{total_others} other {other_suffix}")

            type_summary = natural_join(type_items)

            # Extract Dataset Preview from the first non-empty CSV file
            dataset_preview = ""
            csv_files = [f for f in files if f.lower().endswith(".csv")]
            for target_csv in csv_files:
                csv_path = os.path.join("data", target_csv)
                if os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0:
                    try:
                        with open(csv_path, "r", encoding="utf-8") as f_csv:
                            lines = [line.strip() for line in f_csv if line.strip()]
                        if lines:
                            headers = [col.strip() for col in lines[0].split(",") if col.strip()]
                            row_count = len(lines) - 1

                            missing_col_set = set()
                            # Detect missing values
                            for line in lines[1:]:
                                fields = [f.strip() for f in line.split(",")]
                                if len(fields) < len(headers):
                                    missing_values_count += (len(headers) - len(fields))
                                    for idx in range(len(fields), len(headers)):
                                        missing_col_set.add(headers[idx])
                                for idx, f in enumerate(fields[:len(headers)]):
                                    if f == "":
                                        missing_values_count += 1
                                        missing_col_set.add(headers[idx])

                            missing_val_cols = [h for h in headers if h in missing_col_set]

                            warning_suffix = ""
                            if missing_values_count > 0:
                                cols_str = f" in {', '.join(missing_val_cols)}" if missing_val_cols else ""
                                if args.plain:
                                    warning_suffix = f" ({missing_values_count} missing values{cols_str})"
                                else:
                                    warning_suffix = f" ({EMOJI_WARN}{missing_values_count} missing values{cols_str})"

                            if len(headers) > 6:
                                col_preview = ", ".join(headers[:6]) + ", ..."
                            else:
                                col_preview = ", ".join(headers)
                            dataset_preview = f"{BOLD}{target_csv}{RESET} ({row_count} {'row' if row_count == 1 else 'rows'}){warning_suffix} {SEP} {col_preview}"
                            break
                    except Exception:
                        pass

        # Determine Status and Badge
        if not all_found:
            badge_text = f"[INC:{len(missing_libs)}]"
            badge_color = RED
        elif not data_dir_exists or data_count == 0 or total_size == 0:
            badge_text = "[PEND]"
            badge_color = YELLOW
        else:
            badge_text = "[READY]"
            badge_color = GREEN

        # Print Header
        padding_count = 13 - len(version) - len(badge_text)
        padding = " " * padding_count
        print(border_top)
        print(f"{border_mid_left}{BOLD}Smart Product Analysis{RESET} v{version} {padding}{badge_color}{BOLD}{badge_text}{RESET}{border_mid_right}")
        print(border_bottom)

        # System Status
        print(f"\n{CYAN}{BOLD}System Status:{RESET}")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{BULLET} {'Session Start':<15}: {EMOJI_TIME}{now}")
        os_name = platform.system()
        os_icon = "" if args.plain else ("🐧 " if os_name == "Linux" else "🍎 " if os_name == "Darwin" else "🪟 " if os_name == "Windows" else "")
        print(f"{BULLET} {'System':<15}: {os_icon}{os_name} ({platform.machine()})")
        print(f"{BULLET} {'Python':<15}: {platform.python_version()}")
        env_type = f"{EMOJI_VENV}{BOLD}{GREEN}Virtual Env{RESET}" if is_venv() else f"{EMOJI_GLOBAL}{BOLD}{YELLOW}Global{RESET}"
        print(f"{BULLET} {'Environment':<15}: {env_type}")

        print(f"  {BOLD}Dependencies:{RESET}")
        for label, lib_version in lib_results.items():
            if lib_version:
                status = f"{EMOJI_OK}{BOLD}{GREEN}{lib_version}{RESET}"
            else:
                purpose = libs[label]["purpose"]
                status = f"{EMOJI_ERR}{BOLD}{RED}Not Found{RESET} ({purpose})"
            print(f"  - {label:<13}: {status}")

        if data_dir_exists and data_count > 0:
            suffix = "file" if data_count == 1 else "files"
            size_str = format_size(total_size)
            integrity_warning = f" {BOLD}{YELLOW}{EMOJI_WARN}Files appear empty!{RESET}" if total_size == 0 else ""
            time_diff = time.time() - freshest_time
            is_very_fresh = time_diff < 86400
            is_stale = time_diff > 604800
            fresh_color = GREEN if is_very_fresh else RESET
            warning_str = f" {BOLD}{YELLOW}(Stale?){RESET}" if is_stale else ""
            freshness = f"Updated {BOLD}{fresh_color}{get_relative_time(freshest_time)}{RESET}{warning_str}"
            print(f"{BULLET} {'Data Source':<15}: {EMOJI_OK}{BOLD}{GREEN}Found{RESET} ({data_count} {suffix}, {size_str}){integrity_warning}")
            if 1 <= data_count <= 3:
                file_list = natural_join([f"{BOLD}{f}{RESET} ({format_size(file_sizes.get(f, 0))})" for f in files])
                print(f"  - {'Files':<13}: {file_list}")
            elif data_count > 3:
                latest_size = file_sizes.get(latest_file, 0) if latest_file else 0
                print(f"  - {'Latest':<13}: {BOLD}{latest_file}{RESET} ({format_size(latest_size)})")
            if dataset_preview:
                print(f"  - {'Dataset':<13}: {dataset_preview}")
            print(f"  - {'Composition':<13}: {type_summary}")
            print(f"  - {'Freshness':<13}: {freshness}")
        elif data_dir_exists:
            data_status = f"{EMOJI_WARN}{BOLD}{YELLOW}Empty (0 files){RESET}"
            print(f"{BULLET} {'Data Source':<15}: {data_status}")
        else:
            data_status = f"{EMOJI_ERR}{BOLD}{RED}Not Found{RESET}"
            print(f"{BULLET} {'Data Source':<15}: {data_status}")

        if not all_found:
            lib_suffix = "library" if len(missing_libs) == 1 else "libraries"
            status_msg = f"{EMOJI_ERR}{BOLD}{RED}Incomplete{RESET} ({len(missing_libs)} {lib_suffix} missing) - Please run: {BOLD}pip install -r requirements.txt{RESET}"
        elif not data_dir_exists or data_count == 0:
            status_msg = f"{EMOJI_WARN}{BOLD}{YELLOW}Pending{RESET} - Data directory missing or empty"
        elif total_size == 0:
            status_msg = f"{EMOJI_WARN}{BOLD}{YELLOW}Pending{RESET} - Data files appear empty"
        else:
            status_msg = f"{EMOJI_OK}{BOLD}{GREEN}Ready{RESET}"
        print(f"{BULLET} {'Status':<15}: {status_msg}")

        print(f"\n{EMOJI_ROCKET}Welcome! This tool is designed to help you extract insights from product data.")

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
                print(f"   {connector_color}{connector_sym}{RESET}")
            is_current = False
            this_stage_done = False
            if i == 1:
                if data_count > 0 and total_size > 0:
                    status_tag = f"{BOLD}{GREEN}[DONE]{RESET}"
                    stage_color = GREEN
                    this_stage_done = True
                elif data_count > 0:
                    status_tag = f"{BOLD}{YELLOW}[PEND]{RESET}"
                    stage_color = RESET
                elif all_found:
                    status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
                    stage_color = CYAN
                    is_current = True
                else:
                    status_tag = f"{BOLD}{YELLOW}[PEND]{RESET}"
                    stage_color = RESET
            elif i == 2:
                if data_count > 0 and total_size > 0 and all_found:
                    status_tag = f"{BOLD}{CYAN}[NEXT]{RESET}"
                    stage_color = CYAN
                    is_current = True
                else:
                    status_tag = f"{BOLD}{YELLOW}[PEND]{RESET}"
                    stage_color = RESET
            else:
                status_tag = f"{BOLD}{YELLOW}[PEND]{RESET}"
                stage_color = RESET

            current_indicator = f" {CYAN}{current_indicator_sym}{RESET}" if is_current else ""
            stage_emoji = "" if args.plain else f"{stage['emoji']} "
            print(f"{BOLD}{i}.{RESET} {stage_emoji}{status_tag} {BOLD}{stage_color}{stage['label']:<20}:{RESET} {stage['desc']}{current_indicator}")
            prev_stage_done = this_stage_done

        is_virtual = is_venv()
        if not all_found:
            if len(missing_libs) <= 2:
                missing_list = natural_join([f"{BOLD}{m}{RESET}" for m in missing_libs])
                tip_text = f"Missing {missing_list}? Run {BOLD}pip install -r requirements.txt{RESET} to complete your setup."
            else:
                tip_text = f"{len(missing_libs)} libraries missing? Run the {BOLD}pip install -r requirements.txt{RESET} command to set up your environment."
        elif not data_dir_exists:
            tip_text = f"Almost there! Run {BOLD}python src/main.py --init{RESET} to quickly generate sample data and get started."
            if not is_virtual:
                tip_text += f" (Tip: Use a {BOLD}Virtual Env{RESET} for better management!)"
        elif data_count == 0:
            tip_text = f"Data folder is ready but empty. Run {BOLD}python src/main.py --init{RESET} to populate sample data and get started."
            if not is_virtual:
                tip_text += f" (Tip: Use a {BOLD}Virtual Env{RESET} for better management!)"
        elif total_size == 0:
            tip_text = f"Data files found in {BOLD}data/{RESET} appear to be empty (0 bytes). Please ensure your datasets contain valid product data."
        elif missing_values_count > 0:
            cols_joined = natural_join([f"{BOLD}{c}{RESET}" for c in missing_val_cols]) if missing_val_cols else ""
            in_cols_str = f" in {cols_joined}" if cols_joined else ""
            tip_text = f"Detected {BOLD}{missing_values_count} missing values{RESET}{in_cols_str} in your dataset. Proceed to {BOLD}Stage 2: Data Cleaning{RESET} to handle them!"
        elif not is_virtual:
            tip_text = f"Consider using a {BOLD}Virtual Environment{RESET} for better dependency management. Run {BOLD}python -m venv venv{RESET} to create one!"
        else:
            tip_text = f"{EMOJI_SPARKLES}{BOLD}Everything is set!{RESET} Head over to the {BOLD}Data Cleaning{RESET} stage to prepare your dataset!"

        print(f"\n{EMOJI_TIP}{CYAN}{BOLD}Tip:{RESET} {tip_text}")
        print(f"   Use {BOLD}--help{RESET} or refer to README.md for detailed documentation.")
        print(footer_line)

        # Interactive onboarding prompt
        if not refreshed and all_found and (not data_dir_exists or data_count == 0):
            if hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
                while True:
                    try:
                        response = input(f"\n{EMOJI_SPARKLES}{BOLD}{CYAN}Would you like to initialize the workspace with sample data now? [y/N/help]:{RESET} ").strip().lower()
                        if response in ("?", "h", "help"):
                            print(f"\n{EMOJI_TIP}{CYAN}{BOLD}Help - Workspace Onboarding:{RESET}")
                            print("  Your workspace currently lacks sample product files in the data directory,")
                            print("  preventing data analysis stages (like Cleaning, EDA, etc.) from running.")
                            print("  - If you choose 'yes', we will automatically generate a mock dataset (`data/products.csv`).")
                            print("  - If you choose 'no', you can manually set up the directory or run initialization later using `--init`.\n")
                            continue
                        elif response in ("y", "yes"):
                            csv_path = os.path.join("data", "products.csv")
                            os.makedirs("data", exist_ok=True)
                            sample_data = (
                                "id,name,category,price,stock\n"
                                "1,Smart Watch,Electronics,199.99,50\n"
                                "2,Wireless Earbuds,Electronics,79.99,120\n"
                                "3,Running Shoes,Apparel,89.95,85\n"
                                "4,Leather Wallet,Accessories,35.00,200\n"
                                "5,Coffee Maker,Home,49.99,40\n"
                            )
                            with open(csv_path, "w", encoding="utf-8") as f:
                                f.write(sample_data)

                            print(f"\n{EMOJI_SPARKLES}{BOLD}{GREEN}Initialization complete!{RESET}")
                            print(f"{BULLET} Created {BOLD}data/{RESET} directory.")
                            print(f"{BULLET} Populated {BOLD}data/products.csv{RESET} with sample product datasets.")
                            print(f"{BULLET} Refreshing workspace status...\n")
                            refreshed = True
                            break
                        elif response in ("n", "no", ""):
                            print(f"\n{BOLD}Onboarding declined.{RESET} To start later, you can manually create the {BOLD}data/{RESET} directory or run {BOLD}python src/main.py --init{RESET}!\n")
                            break
                        else:
                            print(f"\n{EMOJI_WARN}{BOLD}{YELLOW}Unrecognized option:{RESET} {BOLD}'{response}'{RESET}. Please enter y, yes, n, no, h, help, or press Enter to decline.\n")
                            continue
                    except (KeyboardInterrupt, EOFError):
                        print(f"\n\n👋 Onboarding interrupted. Exiting gracefully...\n")
                        sys.exit(0)
                if refreshed:
                    continue
        break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted. Exiting gracefully...")
        sys.exit(0)
