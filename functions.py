### Image processing utility ###
# Uses Pillow (PIL) to perform simple image processing operations.

from PIL import Image

### Functions ###

def grayscale(image):
    """Convert an image to grayscale by setting R=G=B for every pixel.
    Note: uses the global width/height variables defined in the main script.
    """
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            image.putpixel((x, y), (r, r, r))
    image.save("output.jpg")

def negative(img):
    """Convert image to its negative by inverting each color channel."""
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (255 - r, 255 - g, 255 - b))
    img.save("output.jpg")

def red_filter(img):
    """Apply a red filter by zeroing green and blue channels."""
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (r, 0, 0))
    img.save("output.jpg")

def increase_brightness(img):
    """Increase brightness by adding a constant to each channel."""
    amount = int(input("How much to increase brightness? "))
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (r + amount, g + amount, b + amount))
    img.save("output.jpg")

def decrease_brightness(img):
    """Decrease brightness by subtracting a constant from each channel."""
    amount = int(input("How much to decrease brightness? "))
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (r - amount, g - amount, b - amount))
    img.save("output.jpg")

def contrast(img):
    """Apply a simple contrast effect using fixed thresholds."""
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            if r < 80:
                r = 0
            elif r > 140:
                r = 255

            if g < 80:
                g = 0
            elif g > 140:
                g = 255

            if b < 80:
                b = 0
            elif b > 140:
                b = 255

            img.putpixel((x, y), (r, g, b))
    img.save("output.jpg")

def thresholding(image):
    """Simple thresholding: channels above threshold -> 255 else -> 0."""
    thresh_r = 123
    thresh_g = 123
    thresh_b = 123
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            r = 255 if r > thresh_r else 0
            g = 255 if g > thresh_g else 0
            b = 255 if b > thresh_b else 0
            image.putpixel((x, y), (r, g, b))
    image.save("output.jpg")

def pixelate(img):
    """Pixelate the image by grouping pixels into blocks of user-specified size."""
    block_size = int(input("Pixelation block size? "))
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            sum_r = sum_g = sum_b = 0
            count = 0
            for dy in range(block_size):
                for dx in range(block_size):
                    ny = y + dy
                    nx = x + dx
                    if ny >= height:
                        ny = height - 1
                    if nx >= width:
                        nx = width - 1
                    r, g, b = img.getpixel((nx, ny))
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    count += 1
            avg_r = int(sum_r // count)
            avg_g = int(sum_g // count)
            avg_b = int(sum_b // count)
            for dy in range(block_size):
                for dx in range(block_size):
                    nx = x + dx
                    ny = y + dy
                    if nx >= width or ny >= height:
                        continue
                    img.putpixel((nx, ny), (avg_r, avg_g, avg_b))
    img.save("output.jpg")

def sepia(img):
    """Apply a sepia tone to the image."""
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            n_r = int(0.393 * r + 0.769 * g + 0.189 * b)
            n_g = int(0.349 * r + 0.686 * g + 0.168 * b)
            n_b = int(0.272 * r + 0.534 * g + 0.131 * b)
            img.putpixel((x, y), (n_r, n_g, n_b))
    img.save("output.jpg")

def smoothing(image):
    """Simple 3x3 average blur (smoothing)."""
    kernel = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            new_r = new_g = new_b = 0
            for ky in range(3):
                for kx in range(3):
                    r, g, b = image.getpixel((x + kx - 1, y + ky - 1))
                    weight = kernel[ky][kx]
                    new_r += int(r * weight)
                    new_g += int(g * weight)
                    new_b += int(b * weight)
            image.putpixel((x, y), (new_r, new_g, new_b))
    image.save("output.jpg")

def sharpen(img):
    """Sharpen image using a simple 3x3 kernel."""
    kernel = [[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]]
    for x in range(1, width - 1):
        for y in range(1, height - 1):
            new_r = new_g = new_b = 0
            for ky in range(3):
                for kx in range(3):
                    r, g, b = img.getpixel((x - 1 + kx, y - 1 + ky))
                    weight = kernel[ky][kx]
                    new_r += int(r * weight)
                    new_g += int(g * weight)
                    new_b += int(b * weight)
            img.putpixel((x, y), (new_r, new_g, new_b))
    img.save("output.jpg")

def gradient(img):
    """Apply a gradient (Sobel-like) filter using a 3x3 kernel."""
    kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    for y in range(0, height - 2):
        for x in range(0, width - 2):
            n_r = n_g = n_b = 0
            for j in range(3):
                for i in range(3):
                    r, g, b = img.getpixel((x + i, y + j))
                    n_r += r * kernel[j][i]
                    n_g += g * kernel[j][i]
                    n_b += b * kernel[j][i]
            img.putpixel((x, y), (n_r, n_g, n_b))
    img.save("output.jpg")

### Main program ###

img = Image.open("img.jpg")
width, height = img.size