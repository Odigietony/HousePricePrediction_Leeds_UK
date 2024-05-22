from flask import Flask, request, render_template, jsonify
from app import app
from app.model import PredictiveModel

 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
       property_type = request.form['property-type']
       state_of_house = request.form['state-of-property']
       year = request.form['year']
       month = request.form['month']
       predicted_value = PredictiveModel.predict(property_type, state_of_house, year, month)
       return jsonify(predicted_value)
    else: 
        return render_template('index.html')
