from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Ajouter le dossier model au path
sys.path.append(os.path.join(os.path.dirname(__file__), "../model"))
import utils

from chatbot import ChatbotAssistant
app = Flask(__name__)
CORS(app)
# ==============================
#  CHATBOT LOADING
# ==============================
chatbot = ChatbotAssistant("server/intent.json")
chatbot.parse_intents()
chatbot.prepare_data()

MODEL_PATH = "server/chatbot_model.pth"
DIM_PATH = "server/dimensions.json"

if os.path.exists(MODEL_PATH) and os.path.exists(DIM_PATH):
    chatbot.load_model(MODEL_PATH, DIM_PATH)
else:
    chatbot.train_model(epochs=200)
    chatbot.save_model(MODEL_PATH, DIM_PATH)

# ==============================
#  EXISTING ENDPOINTS
# ==============================
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


# ==============================
#  CHATBOT ENDPOINT
# ==============================
@app.route('/chatbot', methods=['POST'])
def chatbot_reply():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message missing"}), 400

    reply = chatbot.process_message(user_message)
    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
