from flask import Flask, jsonify
import json

app = Flask(__name__)

#1. Import iamge and process

#After process
# Sample jason data
# class_type = {
#     "contents": [
#         "Seagrass",
#         "Coral",
#         "Seaweeds"
#     ]
# }

# Route to get all data old setup
@app.route('/api/contents', methods=['GET'])    
def get_all_data():
    json_file_path = r'C:\Users\Admin\Documents\TrainYourOwnYOLO\Data\Source_Images\Test_Image_Detection_Results/grouped_detection_results_by_image.json'
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)
