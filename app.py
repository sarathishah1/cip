from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

# Ruta para devolver el JSON
@app.route('/get_json')
def get_json():
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    return jsonify(data)

# Ruta para servir un fichero JSON estático
@app.route('/')
def index():
    return send_from_directory('static', 'example2.json')

