from api_detector import get_all_data
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


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

image_directory = r'C:\Users\Full Scale\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results'
detector_script_path = r'C:\Users\Full Scale\Documents\TrainYourOwnYOLO\3_Inference\Detector.py'


class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(100), nullable=False)
    date_imported = db.Column(db.Date, nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    class_type = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

# Allow all origins (CORS)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def index():
    # Get a list of all image filenames in the directory
    images = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif'))]
    return render_template('index.html', images=images)

#Get all data in database
@app.route('/get_all_data')
def get_all_data():
    all_data = ImageData.query.all()
    data_list = [{
        "id": item.id,
        "image": item.image,
        "date_imported": item.date_imported,
        "latitude": item.latitude,
        "longitude": item.longitude,
        "class_type": item.class_type,
        "status": item.status

        } for item in all_data]
    
    return jsonify(data_list)

# 1. Browse image
@app.route('/browse')
def browse():
    return render_template('browse.html')

def run_detector():
    # Change to the directory where the detector script is located
    os.chdir(os.path.dirname(detector_script_path))
    # Run the detector script
    subprocess.run(['python', 'Detector.py'])

# 2. Image uploaded and start training. Start Detector
@app.route('/train-img')
def trainImg():
    # I will start the Detector.py pointing to the new upload and delete once done.
    # run_detector()
    images = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif'))]
    return render_template('train-img.html', images=images)

@app.route('/images/<filename>')
def get_image(filename):
    # Serve images from the specified directory
    return send_from_directory(image_directory, filename)


@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/gallery-results')
def galleryResults():
    images_directory = 'C:/Users/Full Scale/Documents/TrainYourOwnYOLO/Data/Source_Images/Test_Image_Detection_Results'

    # Get a list of filenames in the directory excluding JSON files
    images = [f for f in os.listdir(images_directory) if os.path.isfile(os.path.join(images_directory, f)) and not f.endswith('.json')]

    # Sort the images by modification time (newest first)
    images.sort(key=lambda f: os.path.getmtime(os.path.join(images_directory, f)), reverse=True)

    return render_template('gallery-results.html', images=images)

@app.route('/media_gallery')
def media_gallery():
    #all_image_data = ImageData.query.all()
    return render_template('media_gallery.html')

@app.route('/charts')
def charts():
    
    data = db.session.query(ImageData.class_type).all()
    # Process the data for the chart
    class_types = [row[0] for row in data]
    unique_class_types = list(set(class_types))
    class_type_counts = [class_types.count(cls) for cls in unique_class_types]

    return render_template('charts.html', labels=unique_class_types, data=class_type_counts)


@app.route('/browse-display')
def browsedisplay():
    return render_template('browse-display.html')

@app.route('/tables')
def tables():
    all_image_data = ImageData.query.all()
    return render_template('tables.html', all_image_data=all_image_data)


@app.route('/seaweed')
def seaweed():
    return render_template('seaweed.html')

@app.route('/seagrass')
def seagrass():
    return render_template('seagrass.html')

@app.route('/coral')
def coral():
    return render_template('coral.html')

# @app.route('/upload')
# def upload():
#     return render_template('upload-img.html')



UPLOAD_FOLDER = r'C:\Users\Full Scale\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'images' not in request.files:
#         return jsonify({'status': 'error', 'message': 'No images provided'}), 400

#     images = request.files.getlist('images')
#     upload_folder = app.config['UPLOAD_FOLDER']

#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)

#     for image in images:
#         image.save(os.path.join(upload_folder, image.filename))

#     return jsonify({'status': 'success', 'message': 'Images uploaded successfully'}), 200



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Fetch JSON data from the API
        api_url = 'http://127.0.0.1:5002/api/contents'
        response = requests.get(api_url)

        if response.status_code == 200:
            api_data = response.json()
            # Assuming the JSON structure is as you provided
            class_type_list = api_data.get("contents", {}).get("contents", [])
        else:
            # Handle the case where the API request fails
            class_type_list = []

        # Access form data
        image = request.files['image']
        date_imported = datetime.strptime(request.form['date_imported'], '%Y-%m-%dT%H:%M')
        #date_imported = datetime.strptime(request.form['date_imported'], '%Y-%m-%d %H:%M:%S.%f')


        latitude = request.form['latitude']
        longitude = request.form['longitude']

        # Convert the list to a JSON string
        class_type_str = ', '.join(class_type_list)

        # Will try to access results from subprocess
        # class_type = request.form['class_type']
        # Instead of using the form data for class_type, use the one obtained from the API
        class_type = class_type_str

        status = request.form['status'] 

        # Save the image to the 'static' folder (create 'static' folder in the same directory as 'app.py')
        image.save(f'static/uploads/{image.filename}')

        # Create a new ImageData instance
        new_image_data = ImageData(image=image.filename, date_imported=date_imported,
                                   latitude=latitude, longitude=longitude,
                                   class_type=class_type, status=status)

        # Add the instance to the database
        db.session.add(new_image_data)
        db.session.commit()

        # Pass the new data to the template for rendering
        return redirect(url_for('check_info', new_data=new_image_data.id))


@app.route('/check-info/<int:new_data>')
def check_info(new_data):
    # Retrieve the newly added data from the database using the provided ID
    new_image_data = db.session.get(ImageData, new_data)
    # Pass the data to the template
    return render_template('check_info.html', new_image_data=new_image_data)


#Fetching data and convert to dictionaries
@app.route('/fetch_markers')
def fetch_markers():
    #Query all data and asign to markers
    markers = ImageData.query.all()
    # Convert markers to a list of dictionaries
    markers_data = [{'latitude': marker.latitude, 'longitude': marker.longitude, 'class_type': marker.class_type} for marker in markers]
    return jsonify({'markers': markers_data})


# class CustomJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         try:
#             if isinstance(obj, datetime):
#                 return obj.isoformat()
#             iterable = iter(obj)
#         except TypeError:
#             pass
#         else:
#             return list(iterable)
#         return JSONEncoder.default(self, obj)

# app.json_encoder = CustomJSONEncoder

# @app.route('/fetch_markers')
# def fetch_markers():
#     # Query all data and assign to markers
#     markers = ImageData.query.all()
#     # Convert markers to a list of dictionaries
#     markers_data = [
#         {
#             'latitude': marker.latitude,
#             'longitude': marker.longitude,
#             'class_type': marker.class_type,
#             'date_imported': marker.date_imported.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',  # Format datetime to ISO
#         }
#         for marker in markers
#     ]
#     return jsonify({'markers': markers_data})


def convert_to_serializable(data):
    if isinstance(data, set):
        return list(data)
    elif isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    else:
        return data

#Get data
@app.route('/api/api_detector_contents')
def api_detector_contents():
    content_list = convert_to_serializable(class_type)
    return jsonify({"contents": class_type})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
