from rembg import remove
from PIL import Image
import io

file_name = "x6"

# Store the path of the image in the variable input_path
input_path = f"{file_name}.png"

# Store the path where the new image with the removed background will be saved in the variable output_path
output_path = f"{input_path}_bgremoved.png"

# Open the image
input_image = Image.open(input_path)

# Convert the image to the format expected by rembg
# rembg expects the input as bytes, so we save the image to a bytes buffer
input_bytes = io.BytesIO()
input_image.save(input_bytes, format=input_image.format)

# Removing the background from the image
output_bytes = remove(input_bytes.getvalue())

# Save the processed image to the output path
# Since the output from rembg is raw image bytes, we need to convert it back to an image
output_image = Image.open(io.BytesIO(output_bytes))
output_image.save(output_path)

print(f"Background removed and saved to {output_path}")
