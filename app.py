from api_detector import contents
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import subprocess
import os
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
    # Pass the data to the template
    return render_template('index.html')

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

# Fetching data and convert to dictionaries
@app.route('/fetch_markers')
def fetch_markers():
    #Query all data and asign to markers
    markers = ImageData.query.all()

    # Convert markers to a list of dictionaries
    markers_data = [{'latitude': marker.latitude, 'longitude': marker.longitude, 'class_type': marker.class_type} for marker in markers]

    # return jsonify({'markers': markers_data})
    return jsonify({'markers': markers_data})

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
    content_list = convert_to_serializable(contents)
    return jsonify({"contents": content_list})

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/gallery')
def gallery():
    #all_image_data = ImageData.query.all()
    return render_template('gallery.html', all_image_data=ImageData)

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/seaweed')
def seaweed():
    return render_template('seaweed.html')

@app.route('/seagrass')
def seagrass():
    return render_template('seagrass.html')

@app.route('/coral')
def coral():
    return render_template('coral.html')

#Get data from the form and submit
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Access form data
        image = request.files['image']
        date_imported = datetime.strptime(request.form['date_imported'], '%Y-%m-%dT%H:%M')
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        
        # Will try to access results from subprocess
        class_type = request.form['class_type']
        #class_type_list = [entry.get("contents") for entry in contents]
        status = request.form['status']

        # Save the image to the 'static' folder (create 'static' folder in the same directory as 'app.py')
        # image.save(f'static/{image.filename}')
        image.save(f'static/uploads/{image.filename}')

        

        # Create a new ImageData instance
        new_image_data = ImageData(image=image.filename, date_imported=date_imported,
                                   latitude=latitude, longitude=longitude,
                                   class_type=class_type, status=status)
        


        # Add the instance to the database
        db.session.add(new_image_data)
        db.session.commit()

        subprocess.run(['python', 'api_deetector.py'])
        # We can get the data here after running the detector.py

        # Pass the new data to the template for rendering
        return redirect(url_for('check_info', new_data=new_image_data.id))

@app.route('/check-info/<int:new_data>')
def check_info(new_data):
    # Retrieve the newly added data from the database using the provided ID
    new_image_data = db.session.get(ImageData, new_data)
    # Pass the data to the template
    return render_template('check_info.html', new_image_data=new_image_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
