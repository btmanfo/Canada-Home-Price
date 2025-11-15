from flask import Flask, request, jsonify
import os
import sys

# Ajouter le dossier model au path
sys.path.append(os.path.join(os.path.dirname(__file__), "../model"))
import utils

app = Flask(__name__)


@app.route('/get_name_element', methods=['GET'])
def get_all_columns():
    columns_name = utils.get_all_columns_data()
    response = jsonify({
        'province': columns_name['province'],
        'city': columns_name['city'],
        'home_type': columns_name['type'],
        'smoking_permission': columns_name['is_smoking']
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    province = request.form['province']
    city = request.form['city']
    home_type = request.form['home_type']
    smoking_permission = request.form['smoking_permission']
    beds = float(request.form['beds'])
    baths = float(request.form['baths'])
    sq_feet = float(request.form['sq_feet'])
    cats = int(request.form['cats'])
    dogs = int(request.form['dogs'])
    nbr_beds = float(request.form['nb_beds'])

    dummies_transformed = {
        "province": province,
        "city": city,
        "home_type": home_type,
        "is_smoking": smoking_permission
    }
    quantified_variables = {
        "beds": beds,
        "baths": baths,
        "sq_feet": sq_feet,
        "cats": cats,
        "dogs": dogs,
        "nbr_beds": nbr_beds
    }

    estimated_price = utils.get_estimation_price(dummies_transformed, quantified_variables)

    response = jsonify({'estimated_price': estimated_price})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
