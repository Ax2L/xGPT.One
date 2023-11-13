from PIL import Image
import svgwrite


def png_to_svg(png_file, svg_file):
    # Open the PNG file
    img = Image.open(png_file)
    img = img.convert("RGBA")

    # Create a new SVG file
    dwg = svgwrite.Drawing(svg_file, profile="tiny")

    # Process each pixel
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            # If the pixel is not transparent
            if pixel[3] > 0:
                # Draw a small circle at the pixel's position
                dwg.add(
                    dwg.circle(
                        center=(x, y),
                        r=0.5,
                        fill=svgwrite.rgb(pixel[0], pixel[1], pixel[2], "%"),
                    )
                )

    # Save the SVG file
    dwg.save()


# Example usage
png_to_svg("helper/converter/input.png", "helper/converter/output.svg")
