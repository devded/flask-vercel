from flask import Flask, request, jsonify
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"Hello": "World"})

@app.route("/parsing", methods=["POST"])
def parsing_text():
    if 'report_img' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['report_img']
    image_bytes = file.read()
    text = process_image(image_bytes)
    return jsonify({"extracted_text": text})

def process_image(image_bytes: bytes) -> str:
    # Convert bytes to numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Extract text using pytesseract
    text = pytesseract.image_to_string(image)
    return text

if __name__ == "__main__":
    app.run(debug=True)
