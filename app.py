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

from sqlalchemy import func
import json


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

#Create database tables
with app.app_context():
    db.create_all()

@app.route('/fetch_and_process_data', methods=['POST'])
def fetch_and_process_data():

    # Access form data
    # date_imported = datetime.strptime(request.form['date_imported'], '%Y-%m-%dT%H:%M')
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Fetch JSON data from the API
    # response = requests.get('http://127.0.0.1:5001/api/jsonContents')
    # data = response.json()

    json_file_path = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results/grouped_detection_results_by_image.json'
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    print(json_data)
    
    for detection_result in json_data:
        confidence = detection_result["confidence"]
        file_path = detection_result["file_path"]
        label = detection_result["label"]
        x_size = detection_result["x_size"]
        xmax = detection_result["xmax"]
        xmin = detection_result["xmin"]
        y_size = detection_result["x_size"]
        ymax = detection_result["xmax"]
        ymin = detection_result["xmin"]

        # Create a new ImageData instance
        new_image_data = DetectionResult(
            # date_imported=date_imported,
            latitude=latitude,
            longitude=longitude,
            file_path=file_path,
            label=label,
            confidence=confidence,
            x_size=x_size,
            xmax=xmax,
            xmin=xmin,
            y_size=y_size,
            ymax=ymax,
            ymin=ymin,
        )

        # Add the instance to the database
        with app.app_context():
            db.session.add(new_image_data)
            db.session.commit()
    # Redirect to a success page or render a template
    return render_template('index.html')

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

# @app.route('/detected-page-message')
# def detected_page_message():
#     image_folder = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results'
#     # Get a list of all image files in the folder
#     image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
#     # Sort the image files by modification time (latest first)
#     latest_image = sorted(image_files, key=lambda x: os.path.getmtime(os.path.join(image_folder, x)), reverse=True)

#     if latest_image:
#         # Get the path of the latest image
#         latest_image_path = os.path.join(image_folder, latest_image[0])
#     else:
#         latest_image_path = None

#     return render_template('detected-page-message.html', latest_image_path=latest_image_path)


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

@app.route('/api/delete_all_data')
def delete_all_data():
    try:
        # Delete all data from the table
        DetectionResult.query.delete()

        # Commit the changes to the database
        db.session.commit()

        response = {'message': 'All data deleted successfully.'}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions appropriately based on your needs
        db.session.rollback()
        response = {'error': str(e)}
        return jsonify(response), 500

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

# @app.route('/charts')
# def charts():
#     data = db.session.query(DetectionResult.label).all()
#     # Process the data for the chart
#     labels = [row[0] for row in data]
#     unique_class_types = list(set(labels))
#     class_type_counts = [labels.count(cls) for cls in unique_class_types]
#     return render_template('charts.html', labels=unique_class_types, data=class_type_counts)


@app.route('/charts')
def charts():
    # Query to get label counts
    label_counts = db.session.query(DetectionResult.label, func.count()).group_by(DetectionResult.label).all()

    # Convert label counts to a dictionary
    labels_data = dict(label_counts)

    return render_template('charts.html', labels_data=labels_data)

@app.route('/label_counts')
def label_counts():
    # Query to get label counts
    label_counts = db.session.query(DetectionResult.label, func.count()).group_by(DetectionResult.label).all()

    # Convert label counts to a dictionary
    labels_data = dict(label_counts)

    return jsonify({'labels': labels_data})

#Display all detected images on this page
@app.route('/browse-display')
def browsedisplay():
    return render_template('browse-display.html')

@app.route('/tables')
def tables():
    all_image_data = DetectionResult.query.all()
    return render_template('tables.html', all_image_data=all_image_data)

    # # Query data sorted by the 'label' column
    # all_image_data = DetectionResult.query.order_by(DetectionResult.label).all()

    # return render_template('tables.html', all_image_data=all_image_data)

        # Query data sorted by the 'label' column
    # results = DetectionResult.query.order_by(DetectionResult.label).all()

    # return render_template('tables.html', results=results)

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
    new_image_data = db.session.get(DetectionResult, new_data)
    # Pass the data to the template
    return render_template('check_info.html', new_image_data=new_image_data)

@app.route('/fetch_markers')
def fetch_markers():
    #Query all data and asign to markers
    markers = DetectionResult.query.all()
    # Convert markers to a list of dictionaries
    markers_data = [{'latitude': marker.latitude, 'longitude': marker.longitude, 'class_type': marker.label, 'confidence':marker.confidence} for marker in markers]
    return jsonify({'markers': markers_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
    # context = ('cert.pem', 'key.pem')  # Use the names of your certificate and key files
    # app.run(host='0.0.0.0', port=5001, ssl_context=context, debug=True)
