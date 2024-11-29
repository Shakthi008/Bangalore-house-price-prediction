from flask import Flask, request, jsonify, render_template
import os
import json
import pickle
import numpy as np

app = Flask(__name__)

__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    base_path = os.path.dirname(__file__)
    columns_path = os.path.join(base_path, "model/columns.json")
    model_path = os.path.join(base_path, "model/banglore_home_prices_model.pickle")

    with open(columns_path, "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    with open(model_path, "rb") as f:
        __model = pickle.load(f)

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    return jsonify({
        'locations': __locations
    })

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    estimated_price = get_estimated_price(location, total_sqft, bhk, bath)
    return jsonify({
        'estimated_price': f"{estimated_price} Lakhs"
    })

if __name__ == "__main__":
    print("Loading artifacts...")
    load_saved_artifacts()
    app.run(debug=True)
