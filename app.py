import os
import uuid

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from database import create_database, save_document, get_documents
from process_document import process_document


# Create Flask application
app = Flask(__name__)

# Create database whenever application starts
create_database()


# Project folder location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(BASE_DIR, "documents", "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "documents", "output")

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}


# Check allowed file extensions
def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Upload route
@app.route("/upload", methods=["POST"])
def upload():

    if "document" not in request.files:
        return "No file uploaded"

    file = request.files["document"]

    if file.filename == "":
        return "Please select a document"

    if not allowed_file(file.filename):
        return "Only PDF, JPG, JPEG and PNG files are allowed"

    original_filename = secure_filename(file.filename)

    unique_filename = (
        uuid.uuid4().hex + "_" + original_filename
    )

    input_path = os.path.join(
        INPUT_FOLDER,
        unique_filename
    )

    file.save(input_path)

    try:

        # Process uploaded document
        extracted_text = process_document(input_path)

        text_filename = (
            os.path.splitext(unique_filename)[0] + ".txt"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            text_filename
        )

        # Save extracted text
        with open(output_path, "w", encoding="utf-8") as output_file:

            output_file.write(extracted_text or "")

        file_type = os.path.splitext(
            original_filename
        )[1].lower()

        # Save document details in database
        save_document(
            original_filename,
            file_type,
            extracted_text
        )

        return render_template(
            "result.html",
            filename=original_filename,
            extracted_text=extracted_text or
            "No text found in this document."
        )

    except Exception as error:

        print("Processing Error:", error)

        return render_template(
            "result.html",
            filename=original_filename,
            extracted_text=f"Processing Error: {error}"
        )
# Document History route
@app.route("/history")
def history():

    documents = get_documents()

    return render_template(
        "history.html",
        documents=documents
    )

# Run application locally
if __name__ == "__main__":

    app.run(debug=True)