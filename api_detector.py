from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

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

        for entry in json_data:
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
                latitude=entry.get('latitude', None),
                longitude=entry.get('longitude', None)
            )
            db.session.add(detection_result)

        # Commit the changes to the database
        db.session.commit()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)
