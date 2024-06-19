import fitz  # PyMuPDF
from PIL import Image

# Define the cropping box based on the provided screenshot
# Coordinates (left, upper, right, lower)
crop_box = (0, 0, 2480, 2690)  # Adjust these values if needed

# Open the PDF file
pdf_document = fitz.open("Newsletter 19th June.pdf")

# Select the first page
page = pdf_document.load_page(0)

# Convert the page to a pixmap (image)
pix = page.get_pixmap(dpi=300)  # Higher DPI for better quality

# Convert the pixmap to a PIL Image
image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Crop the image
cropped_image = image.crop(crop_box)

# Save the cropped image
cropped_image.save("cropped_section.png")
print("Cropped image saved as cropped_section.png")
