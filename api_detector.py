from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thesis.db'  # Replace with your actual database URI
db = SQLAlchemy(app)

class ImageData(db.Model):
    # Your model fields go here
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('testonly.html')

@app.route('/fetch_and_process_data', methods=['POST'])
def fetch_and_process_data():

    # Access form data
    # date_imported = datetime.strptime(request.form['date_imported'], '%Y-%m-%dT%H:%M')
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Fetch JSON data from the API
    response = requests.get('http://127.0.0.1:5001/api/jsonContents')
    data = response.json()

    for detection_result in data:
        confidence = detection_result["confidence"]
        file_path = detection_result["file_path"]
        label = detection_result["label"]


        # Create a new ImageData instance
        new_image_data = ImageData(
            # date_imported=date_imported,
            latitude=latitude,
            longitude=longitude,
            file_path=file_path,
            label=label,
            confidence=confidence,
        )

        # Add the instance to the database
        with app.app_context():
            db.session.add(new_image_data)
            db.session.commit()
    # Redirect to a success page or render a template
    return render_template('img-selected.html')

if __name__ == '__main__':
    app.run(debug=True)
