from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Folder to store uploaded reports
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    return render_template("result.html", filename=file.filename)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)