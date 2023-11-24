from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
data = [
    {"id": 1, "name": "John Doe", "age": 25},
    {"id": 2, "name": "Jane Doe", "age": 30},
    {"id": 3, "name": "Bob Smith", "age": 22}
]

# Route to get all data
@app.route('/api/data', methods=['GET'])
def get_all_data():
    return jsonify({"data": data})

@app.route('/api/names', methods=['GET'])
def get_names():
    names = [entry["name"] for entry in data]
    return jsonify({"names": names})



if __name__ == '__main__':
    app.run(debug=True, port=5002)
