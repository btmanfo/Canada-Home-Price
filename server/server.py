from flask import Flask, request, jsonify
app = Flask(__name__)
import utils

@app.route('/get_name_element', methods = ['GET'])
def get_all_columns():
    columns_name = utils.get_all_columns_data()
    reponse = jsonify({
        'province':columns_name['province'],
        'city': columns_name['city'],
        'home_type': columns_name['type'],
        'smoking_permission': columns_name['is_smoking']
    })
    reponse.headers.add('Access-Control-Allow-Origin', '*')
    return reponse

@app.route('/predict_home_price', methods = ['POST'])
def predict_home_price():
    province = request.form['province']
    city= request.form['city']
    home_type = request.form['home_type']
    smoking_permission = request.form['smoking_permission']
    beds = int(request.form['beds'])
    baths = float(request.form['baths'])
    sq_feet = float(request.form['sq_feet'])
    cats_allowed = int(request.form['cats'])
    dogs_allowed = int(request.form['dogs'])
    #LOL I HAVE DUPLICATE FKKKKK
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
        "cats": cats_allowed,
        "dogs": dogs_allowed,
        'nbr_beds': nbr_beds
    }
    response = jsonify({
        'estimated_price': utils.get_estimation_price(dummies_transformed,quantified_variables)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)