from flask import Flask, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)

# Your base directory
BASE_DIR = r'D:\ForElmo\thesisMapping\FromColabElmoThesis\yolov7\runs\detect'

# Function to recursively get all image files
def get_all_images(directory, subfolder=""):
    images = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            images += get_all_images(entry.path, os.path.join(subfolder, entry.name))
        elif entry.is_file() and (entry.name.endswith('.jpg') or entry.name.endswith('.png') or entry.name.endswith('.jpeg')):
            images.append(os.path.join(subfolder, entry.name))
    return images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images')
def images():
    # Get all images in the directory and subdirectories
    all_images = get_all_images(BASE_DIR)
    return jsonify(all_images)

@app.route('/image/<path:image_path>')
def serve_image(image_path):
    # Safely join the base directory and the image path
    safe_path = os.path.normpath(os.path.join(BASE_DIR, image_path))
    if os.path.exists(safe_path):
        return send_from_directory(os.path.dirname(safe_path), os.path.basename(safe_path))
    else:
        return 'Image does not exist', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)
