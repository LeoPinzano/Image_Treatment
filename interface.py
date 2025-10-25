"""
interface.py - Interactive terminal menu for image filters.

This module provides a CLI and an interactive `main()` to choose and apply
filters from `functions.py`. It supports selecting an input image at runtime
via `-i/--input` or the interactive `-i <path>` command.
"""

import argparse
from PIL import Image
import functions as F

# Optional color support: prefer colorama when available (works on Windows).
try:
    import colorama
    from colorama import Fore, Style

    colorama.init()
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
except Exception:
    # No coloring available — fall back to no-op strings
    RESET = BOLD = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = ""


def _col(text: str, color: str = "") -> str:
    """Wrap text in color codes if available."""
    if not color:
        return text
    return f"{color}{text}{RESET}"

FILTERS = [
    ("Grayscale", F.grayscale),
    ("Negative", F.negative),
    ("Red filter", F.red_filter),
    ("Increase brightness", F.increase_brightness),
    ("Decrease brightness", F.decrease_brightness),
    ("Contrast", F.contrast),
    ("Thresholding", F.thresholding),
    ("Pixelate", F.pixelate),
    ("Sepia", F.sepia),
    ("Smoothing (blur)", F.smoothing),
    ("Sharpen", F.sharpen),
    ("Gradient (edge)", F.gradient),
]

# Session history (recent applied filters) for the running session
session_history = []


def list_filters():
    for i, (name, _) in enumerate(FILTERS, 1):
        num = _col(f"{i}.", CYAN)
        nm = _col(name, BOLD)
        print(f"{num} {nm}")


def show_menu(output_filename: str = None, show_commands: bool = True):
    """Show an improved, full menu with image status, recent actions and commands.

    If show_commands is False, the Commands block will be omitted. This is used
    for the `--list` action which should only show filters/status.
    """
    print(_col("\n=== Filters ===", BOLD + BLUE))
    # Image status
    if hasattr(F, 'img') and F.img is not None:
        try:
            w, h = F.img.size
            print(_col("Image:", GREEN), _col(f"loaded ({w}x{h})", BOLD), _col("- use -i <path> to change", CYAN))
        except Exception:
            print(_col("Image:", YELLOW), _col("(unknown state)", BOLD))
    else:
        print(_col("Image:", YELLOW), _col("(none loaded)", BOLD), _col("- load with -i <path>", CYAN))

    # Output filename
    if output_filename:
        print(_col("Output:", GREEN), _col(output_filename, BOLD))

    # Recent actions
    if session_history:
        recent = ", ".join(session_history[-8:])
        print(_col("Recent:", MAGENTA), _col(recent, BOLD))

    # Filters
    print(_col("\nAvailable filters:", YELLOW))
    for i, (name, _) in enumerate(FILTERS, 1):
        print(f"  {_col(str(i), CYAN)}. {_col(name, BOLD)}")

    # Commands (optional)
    if show_commands:
        print(_col("\nCommands:", YELLOW))
        print("  ", _col("-i <path>", BOLD), "Load input image")
        print("  ", _col("-o <file>", BOLD), "Set output filename")
        print("  ", _col("--list | menu", BOLD), "Show this full menu")
        print("  ", _col("<n,n,...> or <name,name,...>", BOLD), "Apply filters by number or name")
        print("  ", _col("0 | exit | quit", BOLD), "Exit")
        print()


def _load_image(path: str):
    try:
        img = Image.open(path)
        F.img = img
        F.width, F.height = img.size
        print(_col("Loaded image:", GREEN), _col(f"{path}", BOLD), _col(f"({F.width}x{F.height})", CYAN))
        return True
    except Exception as e:
        print(_col("Failed to open:", RED), _col(path, BOLD), "->", _col(str(e), RED))
        return False


def show_welcome():
    """Print a short welcome banner describing the program features."""
    print("\n" + _col("=== Image Treatment - Welcome ===", BOLD + CYAN) + "\n")
    print(_col("This small utility applies simple pixel-based filters to an image using Pillow.", ""))
    print(_col("Features:", YELLOW))
    print("  -", _col("Load an input image", BLUE) + ": use -i/--input on the command line or '-i <path>' in the prompt")
    print("  -", _col("Apply one or more filters", BLUE) + ": by number or name (comma-separated)")
    print("  -", _col("List available filters", BLUE) + ": --list or the prompt command --list")
    print("  -", _col("Save results", BLUE) + ": -o/--output (or set -o at the prompt)")
    print("\n" + _col("Notes:", YELLOW))
    print("  -", _col("Filters operate in place", MAGENTA) + ": final output is saved once.")
    print("  -", _col("Large images may be slow", MAGENTA) + ": consider resizing before heavy operations.")
    print("\n" + _col("Quick example:", GREEN) + "\n  python main.py -i input.jpg -f \"1,sepia\" -o result.jpg\n")


def apply_sequence(tokens, output_filename="output.jpg", input_filename: str = None):
    """Apply a sequence of filter tokens (numbers or names) to the current image.
    If input_filename is provided, load that image first.
    """
    if input_filename:
        if not _load_image(input_filename):
            return

    if not hasattr(F, 'img') or F.img is None:
        print(_col("No image loaded.", YELLOW), "Use", _col("-i/--input", BOLD), "to provide an image first.")
        return

    applied = False
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        # numeric token?
        try:
            n = int(token)
        except Exception:
            n = None

        if n is not None:
            if not (1 <= n <= len(FILTERS)):
                print(_col("Filter number out of range:", RED), _col(str(n), BOLD))
                continue
            name, func = FILTERS[n - 1]
        else:
            matches = [pair for pair in FILTERS if pair[0].lower() == token.lower()]
            if not matches:
                print(_col("No filter named", RED), _col(f"'{token}'", BOLD))
                continue
            name, func = matches[0]

        print(_col("Applying:", YELLOW), _col(name, BOLD), _col("...", YELLOW))
        try:
            func(F.img)
            applied = True
            # record in session history
            session_history.append(name)
        except Exception as e:
            print(_col("Error applying filter", RED), _col(name, BOLD), _col("->", RED), _col(str(e), RED))

    if applied:
        try:
            F.img.save(output_filename)
            print(_col("Saved final image as", GREEN), _col(output_filename, BOLD))
        except Exception as e:
            print(_col("Failed to save result:", RED), _col(str(e), RED))


def main(output_filename: str = "output.jpg", input_filename: str = None):
    """Interactive menu. Enter numbers or names (comma-separated). Commands:
    --list, --help, -o <filename>, -i <path>, exit
    """
    # Show welcome banner
    show_welcome()

    # Load input image if provided
    if input_filename:
        if not _load_image(input_filename):
            return

    if not hasattr(F, 'img') or F.img is None:
        # No image loaded yet; allow user to set image from prompt
        pass

    # Show a compact hint instead of the full menu on startup
    print(_col("Tip:", YELLOW), "Type", _col("--list", BOLD), "to view available filters,", _col("-i <path>", BOLD), "to load an image, or", _col("0", BOLD), "to exit.")

    while True:
        raw = input("Enter command or filter(s) (or --help for commands): ")
        if not raw:
            print("No input provided. Try again.")
            continue

        stripped = raw.strip()
        # support simple command-style inputs entered at the prompt
        if stripped.startswith('-') or stripped.startswith('exit') or stripped.startswith('quit'):
            parts = stripped.split()
            cmd = parts[0]
            if cmd in ('--list', '-l'):
                # show a compact listing (no Commands block) when user requests --list
                show_menu(output_filename, show_commands=False)
                continue
            if cmd in ('--help', '-h'):
                print("Commands:")
                print("  --list, -l          List available filters")
                print("  --help, -h          Show this menu")
                print("  -o <filename>       Set output filename for saved result")
                print("  -i <filename>       Load a different input image")
                print("  exit, quit, 0       Exit the menu")
                continue
            if cmd in ('-o', '--output'):
                if len(parts) >= 2:
                    output_filename = parts[1]
                    print(f"Output filename set to: {output_filename}")
                else:
                    print("Usage: -o <filename>")
                continue
            if cmd in ('-i', '--input'):
                if len(parts) >= 2:
                    fn = parts[1]
                    _load_image(fn)
                else:
                    print("Usage: -i <filename>")
                continue
            if cmd in ('menu', '--menu'):
                show_menu(output_filename)
                continue
            if cmd in ('exit', 'quit', '0'):
                print('Exiting.')
                break

        entries = [t.strip() for t in raw.split(",") if t.strip()]
        if len(entries) == 1 and entries[0] == "0":
            print("Exiting.")
            break

        # Apply chosen filters
        applied_any = False
        for token in entries:
            try:
                n = int(token)
            except Exception:
                n = None

            if n is not None:
                if not (1 <= n <= len(FILTERS)):
                    print(f"Filter number out of range: {n}")
                    continue
                name, func = FILTERS[n - 1]
            else:
                matches = [pair for pair in FILTERS if pair[0].lower() == token.lower()]
                if not matches:
                    print(f"No filter named '{token}' found")
                    continue
                name, func = matches[0]

            print(_col("Applying:", YELLOW), _col(name, BOLD), _col("...", YELLOW))
            try:
                func(F.img)
                applied_any = True
                session_history.append(name)
            except Exception as e:
                print(_col("Error applying filter", RED), _col(name, BOLD), _col("->", RED), _col(str(e), RED))

        if applied_any:
            try:
                F.img.save(output_filename)
                print(f"Saved result as {output_filename}")
            except Exception as e:
                print(f"Failed to save result: {e}")


def cli(argv=None):
    # Disable argparse automatic -h/--help so we can use help to launch the interactive menu
    parser = argparse.ArgumentParser(prog="interface.py", description="Interactive image filter interface", add_help=False)
    # Custom help flag: when passed, open the interactive menu instead of printing the CLI help
    parser.add_argument("-h", "--help", action="store_true", help="show interactive menu (same as --cli)")
    parser.add_argument("--cli", action="store_true", help="launch interactive menu")
    parser.add_argument("--list", action="store_true", help="list available filters")
    parser.add_argument("-f", "--filters", help="comma-separated list of filters (numbers or names)")
    parser.add_argument("-i", "--input", help="input image filename to load before applying filters")
    parser.add_argument("-o", "--output", default="output.jpg", help="output filename (default: output.jpg)")

    args = parser.parse_args(argv)

    # If the user asked for help (-h/--help) we treat that as a request to open the interactive menu
    if args.help:
        main(output_filename=args.output, input_filename=args.input)
        return

    if args.list:
        # For CLI --list, show only the status and filters (hide the Commands block)
        show_menu(args.output, show_commands=False)
        return

    if args.filters:
        tokens = [t.strip() for t in args.filters.split(",") if t.strip()]
        if not tokens:
            print("No filters provided to --filters")
            return
        apply_sequence(tokens, args.output, input_filename=args.input)
        return

    # If --cli requested or no args provided, run interactive menu
    if args.cli or (not any([args.list, args.filters])):
        main(output_filename=args.output, input_filename=args.input)


if __name__ == "__main__":
    cli()