from flask import Flask, request, render_template, jsonify
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load the model
model = YOLO("artifacts/runs/detect/train/weights/best.pt")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    img = Image.open(file.stream)

    img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    results = model(img_cv2)
    # print(results)

    data = {
        "xyxy": [[round(num, 4) for num in inner] for inner in results[0].boxes.xyxy.tolist()],
        "conf": results[0].boxes.conf.tolist()
    }

    # Read and display the image using Matplotlib
    image = results[0].orig_img
    plt.imshow(image)

    # Extract and plot the bounding boxes
    for box, conf in zip(data['xyxy'], data['conf']):
        x1, y1, x2, y2 = box
        plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], label=f'Confidence: {conf}', color='red')

    plt.axis('off')
    # Instead of showing, save the figure
    image_path = 'static/predicted_image.jpg'  # Adjust this path for your setup
    plt.savefig(image_path)
    plt.close()  # Close the figure to free up memory

    with open(image_path, "rb") as img_file:
        img_str = base64.b64encode(img_file.read()).decode('utf-8')

    return jsonify({'image': 'data:image/jpeg;base64,' + img_str})

if __name__ == '__main__':
    app.run(debug=True)
