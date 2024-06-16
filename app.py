from flask import Flask, request, jsonify, render_template
#from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
#CORS(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/filesUsed')
def filesUsed():
    return render_template('filesUsed.html')
@app.route('/theProject')
def theProject():
    return render_template('theProject.html')



@app.route('/process', methods=['POST'])
def process():
    data = request.json
    pais = int(data['pais'])
    renta = int(data['renta'])
    result = pais + renta  # Your processing logic here
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
