from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    pais = int(data['pais'])
    renta = int(data['renta'])
    result = pais + renta  # Your processing logic here
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
