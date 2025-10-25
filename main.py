"""main.py - Runner and entrypoint for image filters.

This file is a lightweight entrypoint. It supports two modes:
- Launch the interactive CLI menu: python main.py --cli
- Apply a specific filter by number or name: python main.py <number|name>

If no arguments are provided the script prints usage instructions.
"""

import argparse
import interface


def main(argv=None):
    parser = argparse.ArgumentParser(prog="main.py", description="Image filters runner")
    parser.add_argument("--cli", action="store_true", help="launch interactive menu")
    parser.add_argument("--list", action="store_true", help="list available filters")
    parser.add_argument("-f", "--filters", help="comma-separated list of filters (numbers or names)")
    parser.add_argument("-i", "--input", help="input image filename to load before applying filters")
    parser.add_argument("-o", "--output", default="output.jpg", help="output filename (default: output.jpg)")

    args = parser.parse_args(argv)

    if args.list:
        interface.list_filters()
        return

    if args.filters:
        tokens = [t.strip() for t in args.filters.split(",") if t.strip()]
        if not tokens:
            print("No filters provided to --filters")
            return
        interface.apply_sequence(tokens, args.output, input_filename=args.input)
        return

    # If --cli was provided, launch interactive menu
    if args.cli:
        interface.main(output_filename=args.output, input_filename=args.input)
        return

    # Default behavior: launch interactive menu (pass input if provided)
    interface.main(output_filename=args.output, input_filename=args.input)


if __name__ == "__main__":
    main()
