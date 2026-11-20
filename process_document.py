from ocr import preprocess_document


def process_document(file_path):

    # Extract text from PDF or image
    extracted_text = preprocess_document(file_path)

    # Split extracted text into lines
    lines = extracted_text.splitlines()

    formatted_lines = []

    for line in lines:

        # Remove extra spaces
        line = " ".join(line.split())

        # Skip empty lines
        if line:

            formatted_lines.append(line)

        else:

            # Preserve paragraph separation
            if formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")

    # Join all lines with proper spacing
    cleaned_text = "\n".join(formatted_lines)

    return cleaned_text.strip()