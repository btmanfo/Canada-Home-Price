import os
import json
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "price_prediction_model.keras")
COLUMNS_PATH = os.path.join(BASE_DIR, "columns_without_classification.json")
ALL_COLUMNS_JSON = os.path.join(BASE_DIR, "columns.json")

__model = load_model(MODEL_PATH)

with open(COLUMNS_PATH, 'r') as f:
    __all_columns_unclassified = json.load(f)


def get_all_columns_data():
    """Retourne les colonnes catégorielles disponibles"""
    with open(ALL_COLUMNS_JSON, 'r') as f:
        return json.load(f)


def get_estimation_price(string_definition: dict, quantity_definition: dict) -> float:
    """Retourne la prédiction du prix en utilisant le modèle Keras"""
    x = np.zeros(len(__all_columns_unclassified) + 7)

    x[__all_columns_unclassified.index(string_definition['province'])] = 1
    x[__all_columns_unclassified.index(string_definition['city'])] = 1
    x[__all_columns_unclassified.index(string_definition['home_type'])] = 1
    x[__all_columns_unclassified.index(string_definition['is_smoking'])] = 1

    x[0] = quantity_definition['beds']
    x[1] = quantity_definition['baths']
    x[2] = quantity_definition['sq_feet']
    x[3] = quantity_definition['cats']
    x[4] = quantity_definition['dogs']
    x[5] = quantity_definition['nbr_beds']

    prediction = __model.predict(np.array([x]))
    return round(float(prediction[0][0]), 2)

if __name__ == "__main__":
    dummies = {'province':'alberta', 'city':'airdrie', 'home_type':'townhouse', 'is_smoking':'non-smoking'}
    quantities = {'beds':2, 'baths':2.5, 'sq_feet':1403.0,'cats':1, 'dogs':1,'nbr_beds':2.0}
    print(get_estimation_price(dummies, quantities))
