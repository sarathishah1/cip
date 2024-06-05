from flask import Flask, jsonify, send_from_directory
import json

app = Flask(__name__)

# Ruta para devolver el JSON
@app.route('/get_json')
def get_json():
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    return jsonify(data)

@app.route('/')
def index():
    with open('./stactic/example2.json', 'r') as f:
        data = json.load(f)
        return jsonify(data)
        

