from flask import Flask, request, jsonify
from SmartRule import SvmModel
from training import predict_output, incremental_train_model
from filter import create_new_filter
from filter import list_filters
import codecs 
import sys 

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/train', methods=['POST'])
def train_def():
    req_dict = request.get_json()
    subject = req_dict['Subject']
    body = req_dict['Body']
    output = req_dict['Output']
    filterName = req_dict['FilterName']

    result = incremental_train_model(filterName, subject, body, output)
    return jsonify({'result' : result})

@app.route('/predict', methods=['POST'])
def predict_def():
    req_dict = request.get_json()
    subject = req_dict['Subject']
    body = req_dict['Body']
    
    print("Predict received")
    print(subject)
    print(body)

    result = predict_output(req_dict)

    return jsonify({'result': result})


@app.route('/createFilter', methods=['POST'])
def create_filter_def():
    req_dict = request.get_json()
    filterName = req_dict['filterName']
    print("creating new filter : " +filterName)
    result = create_new_filter(req_dict)

    return jsonify({'result': result})


@app.route('/listFilters', methods=['GET'])
def list_filter_def():
    print("listing all filters")
    result = list_filters()

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)    

