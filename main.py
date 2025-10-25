"""main.py - Runner and entrypoint for image filters.

This file is a lightweight entrypoint. It supports two modes:
- Launch the interactive CLI menu: python main.py --cli
- Apply a specific filter by number or name: python main.py <number|name>

If no arguments are provided the script prints usage instructions.
"""

import sys
from functions import img, width, height
import interface


def print_usage():
    print("Usage:")
    print("  python main.py --cli            # launch interactive menu")
    print("  python main.py <number>         # apply filter by number (see --list)")
    print("  python main.py --list           # list available filters")
    print("")
    print("Example: python main.py --cli")


def list_filters():
    for i, (name, _) in enumerate(interface.FILTERS, 1):
        print(f"{i}. {name}")


def apply_by_number(n: int):
    if not (1 <= n <= len(interface.FILTERS)):
        print("Filter number out of range")
        return
    name, func = interface.FILTERS[n - 1]
    print(f"Applying: {name} ...")
    func(img)
    print("Done. Saved as output.jpg")


def apply_by_name(name: str):
    for fname, func in interface.FILTERS:
        if fname.lower() == name.lower():
            print(f"Applying: {fname} ...")
            func(img)
            print("Done. Saved as output.jpg")
            return
    print(f"No filter named '{name}' found")


def main():
    if len(sys.argv) == 1:
        print("Image Filter Runner")
        print("Image loaded: img.jpg ({}x{})".format(width, height))
        print_usage()
        return

    arg = sys.argv[1]
    if arg in ("-h", "--help"):
        print_usage()
    elif arg == "--cli":
        interface.main()
    elif arg == "--list":
        list_filters()
    else:
        # try number first
        try:
            n = int(arg)
            apply_by_number(n)
        except ValueError:
            apply_by_name(arg)


if __name__ == "__main__":
    main()
