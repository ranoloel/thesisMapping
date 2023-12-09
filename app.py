# from api_detector import get_all_data
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from datetime import datetime
#from flask.json import JSONEncoder
from datetime import timezone
import subprocess
import os
import json
import requests


#CONSTANTS
#laptop
# UPLOAD_FOLDER = r'C:\Users\Full Scale\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Images'
# image_directory = r'C:\Users\Full Scale\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results'
# detector_script_path = r'C:\Users\Full Scale\Documents\TrainYourOwnYOLO\3_Inference\Detector.py'
# json_file_path = r'C:\Users\Full Scale\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results/grouped_detection_results_by_image.json'

#PC
UPLOAD_FOLDER = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Images'
image_directory = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results'
detector_script_path = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\3_Inference\Detector.py'
json_file_path = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results/grouped_detection_results_by_image.json'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # SQLite database file
db = SQLAlchemy(app)

class DetectionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confidence = db.Column(db.Float)
    file_path = db.Column(db.String(255))
    label = db.Column(db.String(50))
    x_size = db.Column(db.Integer)
    xmax = db.Column(db.Integer)
    xmin = db.Column(db.Integer)
    y_size = db.Column(db.Integer)
    ymax = db.Column(db.Integer)
    ymin = db.Column(db.Integer)
    latitude = db.Column(db.Float)  # Add latitude column
    longitude = db.Column(db.Float)  # Add longitude column

# Create database tables
with app.app_context():
    db.create_all()

    # Check if data already exists in the database
    if DetectionResult.query.count() == 0:
        # Populate the database with JSON data
        json_file_path = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results/grouped_detection_results_by_image.json'
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
        try:
            for entry in json_data:
                # Assuming form_latitude and form_longitude are obtained from your form
                form_latitude = request.form.get('latitude')  # Replace 'latitude' with the actual name of your form field
                form_longitude = request.form.get('longitude')  # Replace 'longitude' with the actual name of your form field
                detection_result = DetectionResult(
                    confidence=entry['confidence'],
                    file_path=entry['file_path'],
                    label=entry['label'],
                    x_size=entry['x_size'],
                    xmax=entry['xmax'],
                    xmin=entry['xmin'],
                    y_size=entry['y_size'],
                    ymax=entry['ymax'],
                    ymin=entry['ymin'],
                    # latitude=entry.get('latitude', None),
                    # longitude=entry.get('longitude', None)
                    latitude=form_latitude,  # Use the value from your form
                    longitude=form_longitude  # Use the value from your form

                )
                db.session.add(detection_result)
            
            # Commit the changes to the database
            db.session.commit()
        except Exception as e:
            print(f"Error: {e}")

# Route to get all data
@app.route('/api/contents', methods=['GET'])
def get_all_data():
    data = DetectionResult.query.all()
    result = []
    for row in data:
        result.append({
            'confidence': row.confidence,
            'file_path': row.file_path,
            'label': row.label,
            'x_size': row.x_size,
            'xmax': row.xmax,
            'xmin': row.xmin,
            'y_size': row.y_size,
            'ymax': row.ymax,
            'ymin': row.ymin,
            'latitude': row.latitude,
            'longitude': row.longitude
        })
    return jsonify(result)

@app.route('/')
def index():
    # Get a list of all image filenames in the directory
    images = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif'))]
    #Clearing all samples once index has been loaded
    delete_test_images()
    print("index: Deleted all sample images")
    return render_template('index.html', images=images)

# 1. Browse image
@app.route('/browse')
def browse():
    return render_template('browse.html')

def run_detector():
    # Change to the directory where the detector script is located
    os.chdir(os.path.dirname(detector_script_path))
    # Run the detector script
    subprocess.run(['python', 'Detector.py'])

@app.route('/waiting-page')
def waitingPage():

    #Calling the detector function that calls the Detector.py
    # run_detector()
    return render_template('waiting-page.html')

@app.route('/detected-page-message')
def detected_page_message():
    #for single image display after running Detector.py
    images_directory = image_directory  # Assuming image_directory is defined
    images = get_sorted_images(images_directory)
    #run Detector.py
    run_detector()
    #When Clicked will proceed to gallery or map options
    return render_template('detected-page-message.html')

@app.route('/gallery-results')
def galleryResults():
    images_directory = image_directory  # Assuming image_directory is defined
    images = get_sorted_images(images_directory)

    # Delete all files in the testing folder
    delete_test_images()
    print("Gallery: Deleted all sample images")

    return render_template('gallery-results.html', images=images)

def get_sorted_images(directory):
    # Get a list of filenames in the directory excluding JSON files
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and not f.endswith('.json')]
    # Sort the images by modification time (newest first)
    images.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
    return images

@app.route('/delete_test_images')
def delete_test_images():
    try:
        # Get a list of all files in the folder
        files = os.listdir(UPLOAD_FOLDER)

        # Loop through the files and delete them
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            os.remove(file_path)

        return 'All files deleted successfully.'

    except Exception as e:
        return f'Error deleting files: {str(e)}'


def userCoordinates():
    #get the lat lng
    #access db and if new data
    #insert lat lang to db
    return 0

@app.route('/images/<filename>')
def get_image(filename):
    # Serve images from the specified directory
    return send_from_directory(image_directory, filename)

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/charts')
def charts():
    data = db.session.query(ImageData.class_type).all()
    # Process the data for the chart
    class_types = [row[0] for row in data]
    unique_class_types = list(set(class_types))
    class_type_counts = [class_types.count(cls) for cls in unique_class_types]
    return render_template('charts.html', labels=unique_class_types, data=class_type_counts)

#Display all detected images on this page
@app.route('/browse-display')
def browsedisplay():
    return render_template('browse-display.html')

@app.route('/tables')
def tables():
    all_image_data = ImageData.query.all()
    return render_template('tables.html', all_image_data=all_image_data)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Form browsing image and send to upload_folder
@app.route('/upload', methods=['POST'])
def upload():
    if 'images' not in request.files:
        return jsonify({'message': 'No images provided'}), 400

    images = request.files.getlist('images')
    upload_folder = app.config['UPLOAD_FOLDER']

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for image in images:
        image.save(os.path.join(upload_folder, image.filename))

    return jsonify({'message': 'Images uploaded successfully'}), 200
    #1.Once done, browser will pop-up with the following js below.
        # - Current date
        # - Lat and lng

@app.route('/check-info/<int:new_data>')
def check_info(new_data):
    # Retrieve the newly added data from the database using the provided ID
    new_image_data = db.session.get(ImageData, new_data)
    # Pass the data to the template
    return render_template('check_info.html', new_image_data=new_image_data)

@app.route('/fetch_markers')
def fetch_markers():
    #Query all data and asign to markers
    markers = ImageData.query.all()
    # Convert markers to a list of dictionaries
    markers_data = [{'latitude': marker.latitude, 'longitude': marker.longitude, 'class_type': marker.class_type} for marker in markers]
    return jsonify({'markers': markers_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
