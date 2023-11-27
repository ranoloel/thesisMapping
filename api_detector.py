from flask import Flask, jsonify

app = Flask(__name__)

#1. Import iamge and process

#After process
# Sample jason data
class_type = {
    "contents": [
        "Coral"
    ]
}

# Route to get all data
@app.route('/api/contents', methods=['GET'])    
def get_all_data():
    return jsonify({"contents": class_type})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)
