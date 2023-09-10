import fitz
from PIL import Image
from fpdf import FPDF
from tkinter import Tk, filedialog
import tempfile
import os

# Create a Tkinter file dialog to select the PDF file
root = Tk()
root.withdraw()  # Hide the main window
file_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
root.destroy()  # Close the Tkinter window
if not file_path:
    print("No PDF file selected.")
    exit()
# Extract PDF pages as images and process them
pdf_document = fitz.open(file_path)
processed_images = []
for page_num in range(len(pdf_document)):
    pdf_page = pdf_document[page_num]
    image = pdf_page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
    # Convert to grayscale and resize image as needed using Pillow
    pil_image = Image.frombytes("RGB", (image.width, image.height), image.samples)
    # resize the file to look like it was scanned
    new_width = int(pil_image.width / 2)
    new_height = int(pil_image.height / 2)
    pil_image = pil_image.resize((new_width, new_height), resample=0)
    old_width = int(new_width) * 2
    old_height = int(new_height) * 2
    pil_image = pil_image.resize((old_width, old_height), resample=0)
    pil_image = pil_image.convert("L")
    processed_images.append(pil_image)

# Create a new PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for img in processed_images:
    # Add a new page
    pdf.add_page()
    # Save the image as a temporary file
    temp_image_path = tempfile.mktemp(suffix=".png")
    img.save(temp_image_path, dpi=(300, 300))
    # Insert the image onto the PDF page
    pdf.image(temp_image_path, x=0, y=0, w=210, h=297)
    # Remove the temporary image file
    os.remove(temp_image_path)

output_file_path = os.path.splitext(file_path)[0] + "_eDoc.pdf"

pdf.output(output_file_path)
