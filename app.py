from flask import Flask, render_template, request
import os
import fitz  # PyMuPDF
import re
from medical_ranges import MEDICAL_RANGES

app = Flask(__name__)

# Folder to store uploaded reports
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Function to extract text from a PDF
def extract_text_from_pdf(filepath):
    """
    Extracts text from a PDF file.

    Parameters:
        filepath (str): Path to the uploaded PDF.

    Returns:
        str: Complete extracted text from the PDF.
    """

    document = fitz.open(filepath)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


# Function to extract medical parameters
def extract_medical_parameters(text):
    """
    Extract important medical parameters from the report.
    Returns a dictionary.
    """

    parameters = {}

    patterns = {
        "Hemoglobin": r"Hemoglobin:\s*([\d.]+)",
        "Glucose": r"Glucose:\s*([\d.]+)",
        "Vitamin D": r"Vitamin D:\s*([\d.]+)",
        "Cholesterol": r"Cholesterol:\s*([\d.]+)"
    }

    for parameter, pattern in patterns.items():

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            parameters[parameter] = match.group(1)

    return parameters


# Function to analyze medical parameters
def analyze_parameters(parameters):
    """
    Compare extracted medical values with reference ranges.
    """

    analysis = {}

    for parameter, value in parameters.items():

        value = float(value)

        if parameter not in MEDICAL_RANGES:
            continue

        reference = MEDICAL_RANGES[parameter]

        if value < reference["low"]:
            status = "Low"

        elif value > reference["high"]:
            status = "High"

        else:
            status = "Normal"

        analysis[parameter] = {
    "value": value,
    "status": status,
    "unit": reference["unit"],
    "low": reference["low"],
    "high": reference["high"]
}

    return analysis


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "report" not in request.files:
        return "No file selected."

    file = request.files["report"]

    if file.filename == "":
        return "No file selected."

    # Save uploaded file
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(filepath)

    print("\n========== EXTRACTED TEXT ==========\n")
    print(extracted_text)
    print("\n====================================\n")

    # Extract medical parameters
    parameters = extract_medical_parameters(extracted_text)

    print("\n===== MEDICAL PARAMETERS =====\n")

    for key, value in parameters.items():
        print(f"{key}: {value}")

    print("\n==============================\n")

    # Analyze medical parameters
    analysis = analyze_parameters(parameters)

    print("\n===== ANALYSIS RESULTS =====\n")

    for parameter, result in analysis.items():

        print(
            f"{parameter}: "
            f"{result['value']} {result['unit']} "
            f"-> {result['status']}"
        )

    print("\n============================\n")

    return render_template(
    "result.html",
    filename=file.filename,
    analysis=analysis
)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True
    )