import os
import json
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model/price_prediction_model.keras")
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
    x = np.zeros(6 + len(__all_columns_unclassified))  # 54 colonnes total

    x[0] = quantity_definition["baths"]
    x[1] = quantity_definition["sq_feet"]
    x[2] = quantity_definition["cats"]
    x[3] = quantity_definition["dogs"]
    x[4] = quantity_definition["nbr_beds"]

    x[5] = quantity_definition["sq_feet"] and quantity_definition["baths"]
    offset = 6

    for key in ["province", "city", "home_type", "is_smoking"]:
        value = string_definition[key].lower()

        if value in __all_columns_unclassified:
            col_idx = __all_columns_unclassified.index(value)
            x[offset + col_idx] = 1
        else:
            print("WARNING: valeur inconnue →", value)

    # === PREDICTION ===
    prediction = __model.predict(np.array([x]))
    return float(prediction[0][0])
    
if __name__ == "__main__":
    dummies = {'province':'alberta', 'city':'airdrie', 'home_type':'townhouse', 'is_smoking':'non-smoking'}
    quantities = {'beds':2, 'baths':2.5, 'sq_feet':1403.0,'cats':1, 'dogs':1,'nbr_beds':2.0}
    print(get_estimation_price(dummies, quantities))
