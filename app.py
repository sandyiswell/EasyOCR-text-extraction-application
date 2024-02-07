from flask import Flask, render_template, request
import numpy as np
import cv2
import easyocr

app = Flask(__name__)

# variables for max height and width
max_height = 1500
max_width = 1500


def ocr_receipt_details(image):
    # global max_height, max_width

    height, width = image.shape[:2]

    # Check if resizing is required
    if height > max_height or width > max_width:
        resized_img = resize_image(image)
        gray_image = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using EasyOCR
    reader = easyocr.Reader(['en'])
    results = reader.readtext(gray_image)

    # Prepare results
    ocr_results = []
    for (bbox, text, prob) in results:
        """(top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        ocr_results.append({'text': text, 'probability': prob, 'bounding_box': (top_left, bottom_right)})"""
        # ocr_results.append({'text': text})
        ocr_results.append(text)
        # print("text is: ", text)
    return ocr_results



def resize_image(loaded_img):
    # global max_height, max_width
    img_height, img_width = loaded_img.shape[:2]

    aspect_ratio = img_width / img_height

    if aspect_ratio > 1:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        new_height = max_height
        new_width = int(max_height * aspect_ratio)

    resized_img = cv2.resize(loaded_img, (new_width, new_height))
    return resized_img


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        # return jsonify({'error': 'No file selected'})
        return "No selected file"

    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    ocr_result_text = ocr_receipt_details(image)
    return render_template('result.html', ocr_result_text=ocr_result_text)

if __name__ == '__main__':
    app.run(debug=True)