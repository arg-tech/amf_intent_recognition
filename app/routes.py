from flask import request, render_template, Response
from . import application
import json
import os
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
