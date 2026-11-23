import os
import re
import shutil
import time
import fitz
import pytesseract

from PIL import Image, ImageOps, ImageEnhance
from pytesseract import Output


# Tesseract path configuration
if os.name == "nt":

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

else:

    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# Check Tesseract only when OCR is required
def check_tesseract():

    path = pytesseract.pytesseract.tesseract_cmd

    if not os.path.isfile(path) and not shutil.which(path):

        raise FileNotFoundError(
            "Tesseract OCR is not installed or path is incorrect."
        )


# Image preprocessing
def improve_image(image):

    image = image.convert("RGB")

    width, height = image.size

    image = image.resize(
        (width * 2, height * 2),
        Image.Resampling.LANCZOS
    )

    image = ImageOps.grayscale(image)

    image = ImageOps.autocontrast(image)

    image = ImageEnhance.Sharpness(image).enhance(2.0)

    return image


# Extract text from images using OCR
def extract_ordered_text(image):

    image = improve_image(image)

    data = pytesseract.image_to_data(
        image,
        config="--oem 3 --psm 11",
        output_type=Output.DICT
    )

    lines = {}

    for i in range(len(data["text"])):

        word = data["text"][i].strip()

        try:
            confidence = float(data["conf"][i])
        except (ValueError, TypeError):
            continue

        if not word or confidence < 20:
            continue

        block = data["block_num"][i]
        paragraph = data["par_num"][i]
        line = data["line_num"][i]

        key = (block, paragraph, line)

        if key not in lines:
            lines[key] = []

        lines[key].append((
            data["left"][i],
            word
        ))

    output = []

    for key in sorted(lines.keys()):

        words = sorted(
            lines[key],
            key=lambda item: item[0]
        )

        line_text = " ".join(
            item[1] for item in words
        )

        output.append(line_text)

    return "\n".join(output)


# Clean extracted text
def clean_text(text):

    cleaned_lines = []

    for line in text.splitlines():

        line = line.strip()

        line = re.sub(r"[ \t]+", " ", line)

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# Main document processing function
def process_document(file_path):

    start_time = time.perf_counter()

    extension = os.path.splitext(file_path)[1].lower()

    extracted_text = []

    # Process PDF
    if extension == ".pdf":

        pdf = fitz.open(file_path)

        try:

            print("Total PDF pages:", len(pdf))

            for page_number, page in enumerate(pdf):

                page_start = time.perf_counter()

                # Direct extraction for text-based PDF
                page_text = page.get_text(
                    "text",
                    sort=True
                )

                if page_text.strip():

                    extracted_text.append(page_text)

                    print(
                        f"Page {page_number + 1}: "
                        "Digital text extracted"
                    )

                else:

                    # OCR only for scanned pages
                    print(
                        f"Page {page_number + 1}: "
                        "Scanned page detected"
                    )

                    check_tesseract()

                    pix = page.get_pixmap(
                        matrix=fitz.Matrix(2, 2),
                        alpha=False
                    )

                    image = Image.frombytes(
                        "RGB",
                        [pix.width, pix.height],
                        pix.samples
                    )

                    text = extract_ordered_text(image)

                    extracted_text.append(text)

                print(
                    f"Page processing time: "
                    f"{time.perf_counter() - page_start:.2f} seconds"
                )

        finally:

            pdf.close()

    # Process image files
    elif extension in [".png", ".jpg", ".jpeg"]:

        check_tesseract()

        image = Image.open(file_path)

        text = extract_ordered_text(image)

        extracted_text.append(text)

        image.close()

    else:

        raise ValueError(
            "Only PDF, PNG, JPG and JPEG files are supported."
        )

    # Combine extracted pages
    final_text = "\n\n".join(extracted_text)

    # Clean extracted text
    final_text = clean_text(final_text)

    print(
        "Total document processing time:",
        round(time.perf_counter() - start_time, 2),
        "seconds"
    )

    return final_text