from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
{
    "class_type": [
        "Coral",
        "Coral",
        "Seaweed",
        "Others-NPS"
    ]
}
# Route to get all data
@app.route('/api/contents', methods=['GET'])
def get_all_data():
    return jsonify({"contents": contents})

@app.route('/api/names', methods=['GET'])
def get_names():
    names = [entry["name"] for entry in data]
    return jsonify({"names": names})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
