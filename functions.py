from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

def pdf_to_text(pdf_path):
    # Step 1: Convert PDF to images
    images = convert_from_path(pdf_path)

    with open('output.txt', 'w') as f:  # Open the text file in write mode
        for i, image in enumerate(images):
            # Save pages as images in the pdf
            image_file = f'page{i}.jpg'
            image.save(image_file, 'JPEG')

            # Step 2: Use OCR to extract text from images
            text = pytesseract.image_to_string(image_file)

            f.write(text + '\n')  # Write the text to the file and add a newline for each page

def load_txt_data(uploaded_file):
    with open('uploaded_file.txt', 'w') as f:
        f.write(uploaded_file.getvalue().decode())
    return uploaded_file.getvalue().decode()

def load_pdf_data(uploaded_file):
    with open('uploaded_file.pdf', 'wb') as f:
        f.write(uploaded_file.getbuffer())
    pdf = PdfReader('uploaded_file.pdf')
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    pdf_to_text('uploaded_file.pdf')
    return text