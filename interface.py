"""
interface.py - Interactive terminal menu for image filters.

This module provides a CLI and an interactive `main()` to choose and apply
filters from `functions.py`. It supports selecting an input image at runtime
via `-i/--input` or the interactive `-i <path>` command.
"""

import argparse
from PIL import Image
import functions as F

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


def list_filters():
    for i, (name, _) in enumerate(FILTERS, 1):
        print(f"{i}. {name}")


def _load_image(path: str):
    try:
        img = Image.open(path)
        F.img = img
        F.width, F.height = img.size
        print(f"Loaded image: {path} ({F.width}x{F.height})")
        return True
    except Exception as e:
        print(f"Failed to open '{path}': {e}")
        return False


def show_welcome():
    """Print a short welcome banner describing the program features."""
    print("\n=== Image Treatment - Welcome ===\n")
    print("This small utility applies simple pixel-based filters to an image using Pillow.")
    print("Features:")
    print("  - Load an input image: use -i/--input on the command line or '-i <path>' in the prompt")
    print("  - Apply one or more filters by number or name (comma-separated)")
    print("  - List available filters with --list or the prompt command --list")
    print("  - Save results with -o/--output (or set -o at the prompt)")
    print("\nNotes:")
    print("  - Filters operate in place on the loaded image; the final output is saved once.")
    print("  - Large images may be slow; consider resizing before heavy operations.")
    print("\nQuick example:\n  python main.py -i input.jpg -f \"1,sepia\" -o result.jpg\n")


def apply_sequence(tokens, output_filename="output.jpg", input_filename: str = None):
    """Apply a sequence of filter tokens (numbers or names) to the current image.
    If input_filename is provided, load that image first.
    """
    if input_filename:
        if not _load_image(input_filename):
            return

    if not hasattr(F, 'img') or F.img is None:
        print("No image loaded. Use -i/--input to provide an image first.")
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
                print(f"Filter number out of range: {n}")
                continue
            name, func = FILTERS[n - 1]
        else:
            matches = [pair for pair in FILTERS if pair[0].lower() == token.lower()]
            if not matches:
                print(f"No filter named '{token}' found")
                continue
            name, func = matches[0]

        print(f"Applying: {name} ...")
        try:
            func(F.img)
            applied = True
        except Exception as e:
            print(f"Error applying filter '{name}': {e}")

    if applied:
        try:
            F.img.save(output_filename)
            print(f"Saved final image as {output_filename}")
        except Exception as e:
            print(f"Failed to save result: {e}")


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
        print("No image loaded. Use -i <path> or run with -i/--input <path> to load an image.")
        # still allow user to set image from prompt

    print("Image Filter CLI\n==================")
    while True:
        try:
            iw, ih = F.img.size
            print(f"Image loaded: ({iw}x{ih})")
        except Exception:
            print("Image loaded: (none)")
        print("\nChoose a filter to apply (you can enter multiple, separated by commas):")
        for i, (name, _) in enumerate(FILTERS, 1):
            print(f"  {i}. {name}")
        print("  0. Exit")
        raw = input("Enter number(s) or name(s), or 0 to exit (or --help for commands): ")
        if not raw:
            print("No input provided. Try again.")
            continue

        stripped = raw.strip()
        # support simple command-style inputs entered at the prompt
        if stripped.startswith('-') or stripped.startswith('exit') or stripped.startswith('quit'):
            parts = stripped.split()
            cmd = parts[0]
            if cmd in ('--list', '-l'):
                list_filters()
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

            print(f"Applying: {name} ...")
            try:
                func(F.img)
                applied_any = True
            except Exception as e:
                print(f"Error applying filter '{name}': {e}")

        if applied_any:
            try:
                F.img.save(output_filename)
                print(f"Saved result as {output_filename}")
            except Exception as e:
                print(f"Failed to save result: {e}")


def cli(argv=None):
    parser = argparse.ArgumentParser(prog="interface.py", description="Interactive image filter interface")
    parser.add_argument("--cli", action="store_true", help="launch interactive menu")
    parser.add_argument("--list", action="store_true", help="list available filters")
    parser.add_argument("-f", "--filters", help="comma-separated list of filters (numbers or names)")
    parser.add_argument("-i", "--input", help="input image filename to load before applying filters")
    parser.add_argument("-o", "--output", default="output.jpg", help="output filename (default: output.jpg)")

    args = parser.parse_args(argv)

    if args.list:
        list_filters()
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