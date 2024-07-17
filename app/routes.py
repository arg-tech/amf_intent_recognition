from flask import request, render_template
from . import application
import json
from app.amf_nts import generate_predictions_amf_nts
from app.amf_ts import generate_predictions_amf_ts

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
        #return render_template('README.md')

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

if __name__ == '__main__':
    application.run(debug=True)
