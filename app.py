from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False)
    date_imported = db.Column(db.Date, nullable=False)
    latitude = db.Column(db.String(20), nullable=False)
    longitude = db.Column(db.String(20), nullable=False)
    class_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    # Query all data from the ImageData table
    all_image_data = ImageData.query.all()
    
    # Pass the data to the template
    return render_template('input-file.html', all_image_data=all_image_data)


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
        image.save(f'D:/TrainYourOwnYOLO/Data/Source_Images/Test_Images/{image.filename}')

        # Create a new ImageData instance
        new_image_data = ImageData(image=image.filename, date_imported=date_imported,
                                   latitude=latitude, longitude=longitude,
                                   class_type=class_type, status=status)

        # Add the instance to the database
        db.session.add(new_image_data)
        db.session.commit()

        subprocess.run(['python', 'D:/TrainYourOwnYOLO/3_Inference/Detector.py'])

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
