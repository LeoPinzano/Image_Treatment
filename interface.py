"""
interface.py - Interactive terminal menu for image filters.

This module provides `main()` which launches a simple text menu to choose
and apply filters from `functions.py`.
"""

import argparse
import sys
from functions import (
    img, width, height,
    grayscale, negative, red_filter, increase_brightness, decrease_brightness,
    contrast, thresholding, pixelate, sepia, smoothing, sharpen, gradient
)

FILTERS = [
    ("Grayscale", grayscale),
    ("Negative", negative),
    ("Red filter", red_filter),
    ("Increase brightness", increase_brightness),
    ("Decrease brightness", decrease_brightness),
    ("Contrast", contrast),
    ("Thresholding", thresholding),
    ("Pixelate", pixelate),
    ("Sepia", sepia),
    ("Smoothing (blur)", smoothing),
    ("Sharpen", sharpen),
    ("Gradient (edge)", gradient),
]


def main(output_filename: str = "output.jpg"):
    """Interactive menu. User may enter a single number or multiple comma-separated
    values (e.g. "1,3,sepia") which will be applied sequentially. Results are
    saved to `output_filename` after applying the selected filters.
    """
    print("Image Filter CLI\n==================")
    print("Image loaded: img.jpg ({}x{})".format(width, height))
    while True:
        print("\nChoose a filter to apply (you can enter multiple, separated by commas):")
        for i, (name, _) in enumerate(FILTERS, 1):
            print(f"  {i}. {name}")
        print("  0. Exit")
        raw = input("Enter number(s) or name(s), or 0 to exit (or --help for commands): ")
        if not raw:
            print("No input provided. Try again.")
            continue
        # support simple command-style inputs entered at the prompt
        # e.g. --list, --help, -o filename
        stripped = raw.strip()
        if stripped.startswith('-'):
            parts = stripped.split()
            cmd = parts[0]
            if cmd in ('--list', '-l'):
                list_filters()
                continue
            if cmd in ('--help', '-h'):
                print("Commands:")
                print("  --list, -l          List available filters")
                print("  --help, -h          Show this help")
                print("  -o <filename>       Set output filename for saved result")
                print("  exit, quit, 0       Exit the menu")
                continue
            if cmd in ('-o', '--output'):
                if len(parts) >= 2:
                    output_filename = parts[1]
                    print(f"Output filename set to: {output_filename}")
                else:
                    print("Usage: -o <filename>")
                continue
            if cmd in ('exit', 'quit'):
                print('Exiting.')
                break
        entries = [t.strip() for t in raw.split(",") if t.strip()]
        if len(entries) == 1 and entries[0] == "0":
            print("Exiting.")
            break

        applied_any = False
        for token in entries:
            # try numeric
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
                # try to match by name (case-insensitive)
                matches = [pair for pair in FILTERS if pair[0].lower() == token.lower()]
                if not matches:
                    print(f"No filter named '{token}' found")
                    continue
                name, func = matches[0]

            print(f"Applying: {name} ...")
            try:
                func(img)
                applied_any = True
            except Exception as e:
                print(f"Error applying filter '{name}': {e}")

        if applied_any:
            try:
                img.save(output_filename)
                print(f"Saved result as {output_filename}")
            except Exception as e:
                print(f"Failed to save result: {e}")


    def list_filters():
        for i, (name, _) in enumerate(FILTERS, 1):
            print(f"{i}. {name}")


    def apply_sequence(tokens, output_filename="output.jpg"):
        """Apply a sequence of tokens (numbers or names) to the module-level `img`.
        Tokens is an iterable of strings. Saves final image to output_filename.
        """
        applied = False
        for token in tokens:
            token = token.strip()
            if not token:
                continue
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
                func(img)
                applied = True
            except Exception as e:
                print(f"Error applying filter '{name}': {e}")

        if applied:
            try:
                img.save(output_filename)
                print(f"Saved final image as {output_filename}")
            except Exception as e:
                print(f"Failed to save result: {e}")


    def cli(argv=None):
        parser = argparse.ArgumentParser(prog="interface.py", description="Interactive image filter interface")
        parser.add_argument("--cli", action="store_true", help="launch interactive menu")
        parser.add_argument("--list", action="store_true", help="list available filters")
        parser.add_argument("-f", "--filters", help="comma-separated list of filters (numbers or names)")
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
            apply_sequence(tokens, args.output)
            return

        # If --cli requested or no args provided, run interactive menu
        if args.cli or (not any([args.list, args.filters])):
            main(output_filename=args.output)


    if __name__ == "__main__":
        cli()