"""
main.py - Terminal interface for image filters

Usage:
- Ensure 'img.jpg' exists in the same folder.
- Run: python main.py
- Choose a filter from the menu; result is saved as 'output.jpg'.
"""

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

def main():
    print("Image Filter CLI\n==================")
    print("Image loaded: img.jpg ({}x{})".format(width, height))
    while True:
        print("\nChoose a filter to apply:")
        for i, (name, _) in enumerate(FILTERS, 1):
            print(f"  {i}. {name}")
        print("  0. Exit")
        try:
            choice = int(input("Enter number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if choice == 0:
            print("Exiting.")
            break
        if 1 <= choice <= len(FILTERS):
            filter_name, filter_func = FILTERS[choice - 1]
            print(f"Applying: {filter_name} ...")
            try:
                filter_func(img)
                print("Done! Saved as output.jpg.")
            except Exception as e:
                print(f"Error applying filter: {e}")
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
