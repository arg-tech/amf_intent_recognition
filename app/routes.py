from flask import redirect, request, render_template, jsonify
from . import application
import json
from app.xaif import generate_predictions

@application.route('/ya_predict', methods=['GET', 'POST'])
def amf_schemes():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        ff = open(f.filename, 'r')
        content = json.load(ff)
        predictions = generate_predictions(content)
        return (predictions)
    elif request.method == 'GET':
        return render_template('index.html')