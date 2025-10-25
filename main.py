"""main.py - Runner and entrypoint for image filters.

This file is a lightweight entrypoint. It supports two modes:
- Launch the interactive CLI menu: python main.py --cli
- Apply a specific filter by number or name: python main.py <number|name>

If no arguments are provided the script prints usage instructions.
"""

import argparse
import sys
from functions import img, width, height
import interface


def list_filters():
    for i, (name, _) in enumerate(interface.FILTERS, 1):
        print(f"{i}. {name}")


def apply_sequence(tokens, output_filename):
    """Apply a sequence of tokens (numbers or names) to the module-level `img`.
    Tokens is an iterable of strings. Saves final image to output_filename.
    """
    applied = False
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        # try numeric
        try:
            n = int(token)
        except Exception:
            n = None

        if n is not None:
            if not (1 <= n <= len(interface.FILTERS)):
                print(f"Filter number out of range: {n}")
                continue
            name, func = interface.FILTERS[n - 1]
        else:
            matches = [pair for pair in interface.FILTERS if pair[0].lower() == token.lower()]
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


def main(argv=None):
    parser = argparse.ArgumentParser(prog="main.py", description="Image filters runner")
    parser.add_argument("--cli", action="store_true", help="launch interactive menu")
    parser.add_argument("--list", action="store_true", help="list available filters")
    parser.add_argument("-f", "--filters", help="comma-separated list of filters (numbers or names)")
    parser.add_argument("-o", "--output", default="output.jpg", help="output filename (default: output.jpg)")

    args = parser.parse_args(argv)

    # If --list was provided, list and exit
    if args.list:
        list_filters()
        return

    # If filters were passed non-interactively, apply them and exit
    if args.filters:
        tokens = [t.strip() for t in args.filters.split(",") if t.strip()]
        if not tokens:
            print("No filters provided to --filters")
            return
        apply_sequence(tokens, args.output)
        return

    # If --cli was provided, launch interactive menu
    if args.cli:
        interface.main(output_filename=args.output)
        return

    # Default behavior: no explicit options -> launch interactive menu
    interface.main(output_filename=args.output)


if __name__ == "__main__":
    main()
