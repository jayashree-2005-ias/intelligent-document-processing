import os
import fitz
import pytesseract

from PIL import Image
from preprocess import preprocess_image


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def preprocess_document(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    extracted_text = ""

    # PDF processing
    if extension == ".pdf":

        pdf = fitz.open(file_path)

        for page in pdf:

            # Convert PDF page into image
            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2),
                alpha=False
            )

            image = Image.frombytes(
                "RGB",
                (pix.width, pix.height),
                pix.samples
            )

            # Preprocess image
            processed_image = preprocess_image(image)

            # Extract text
            text = pytesseract.image_to_string(
                processed_image,
                lang="eng"
            )

            extracted_text += text + "\n"

        pdf.close()

    # Image processing
    elif extension in [".jpg", ".jpeg", ".png"]:

        image = Image.open(file_path).convert("RGB")

        processed_image = preprocess_image(image)

        extracted_text = pytesseract.image_to_string(
            processed_image,
            lang="eng"
        )

    else:

        raise ValueError("Unsupported document format")

    return extracted_text