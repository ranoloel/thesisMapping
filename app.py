from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import subprocess

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
    class_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    # Query all data from the ImageData table
    #all_image_data = ImageData.query.all()
    
    # Pass the data to the template
    return render_template('index.html')

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

# Example route for fetching marker data
@app.route('/fetch_markers')
def fetch_markers():
    markers = ImageData.query.all()

    # Convert markers to a list of dictionaries
    markers_data = [{'latitude': marker.latitude, 'longitude': marker.longitude, 'class_type': marker.class_type} for marker in markers]

    # return jsonify({'markers': markers_data})
    return jsonify({'markers': markers_data})

# @app.route('/sample')
# def sample():
#     return render_template('sample.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/gallery')
def gallery():
    
    all_image_data = ImageData.query.all()
    return render_template('gallery.html', all_image_data=all_image_data)

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

        subprocess.run(['python', 'NotThisDetector.py'])

        # Pass the new data to the template for rendering
        return redirect(url_for('check_info', new_data=new_image_data.id))

@app.route('/check-info/<int:new_data>')
def check_info(new_data):
    # Retrieve the newly added data from the database using the provided ID
    new_image_data = db.session.get(ImageData, new_data)

    # Pass the data to the template
    return render_template('check_info.html', new_image_data=new_image_data)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
