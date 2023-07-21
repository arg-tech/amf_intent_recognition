from flask import request, render_template, Response
from . import application
import json
import os
from app.amf_nts import generate_predictions_amf_nts
from app.amf_ts import generate_predictions_amf_ts
from app.signature_nts import generate_predictions_signature_nts
from app.signature_ts import generate_predictions_signature_ts
from app.signature_evaulation_1 import generate_predictions_signature_evaulation_1

@application.route('/amf_nts', methods=['GET', 'POST'])
def amf_nts():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        ff = open(f.filename, 'r')
        content = json.load(ff)
        predictions = generate_predictions_amf_nts(content)
        return (predictions)
    elif request.method == 'GET':
        return render_template('index_amf_nts.html')
    
@application.route('/amf_ts', methods=['GET', 'POST'])
def amf_ts():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        ff = open(f.filename, 'r')
        content = json.load(ff)
        predictions = generate_predictions_amf_ts(content)
        return (predictions)
    elif request.method == 'GET':
        return render_template('index_amf_ts.html')
    
@application.route('/signature_nts', methods=['GET', 'POST'])
def signature_nts():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        ff = open(f.filename, 'r')
        content = json.load(ff)
        predictions = generate_predictions_signature_nts(content)
        return (predictions)
    elif request.method == 'GET':
        return render_template('index_signature_nts.html')
    
@application.route('/signature_ts', methods=['GET', 'POST'])
def signature_ts():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        ff = open(f.filename, 'r')
        content = json.load(ff)
        predictions = generate_predictions_signature_ts(content)
        return (predictions)
    elif request.method == 'GET':
        return render_template('index_signature_ts.html')
    
@application.route('/signature_evaulation_1', methods=['GET', 'POST'])
def signature_eval_1():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        ff = open(f.filename, 'r')
        content = json.load(ff)
        predictions = generate_predictions_signature_evaulation_1(content)
        return (predictions)
    elif request.method == 'GET':
        return render_template('index_signature_eval_1.html')

# for the n8n system to convert from bjson back to json
@application.route('/bson_json', methods=['GET', 'POST'])
def remove_backslashes():
    if request.method == 'POST':
        fi = request.files['filei']
        fi.save(fi.filename)
        ffi = open(fi.filename, 'r')
        content = ffi.read()
        # Remove the backslashes
        data = content.replace('\\', '')
        #predictions = generate_predictions(data)
        #return data
        # Determine the file format of the input data
        _, file_extension = os.path.splitext(fi.filename)
        # Return the data with the file format
        return Response(data, mimetype=f'application/{file_extension[1:]}')
    elif request.method == 'GET':
        return render_template('bjson.html')
    
if __name__ == '__main__':
    application.run(debug=True)
