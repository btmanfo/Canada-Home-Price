import json
import pickle
import numpy as np
import os
__all_columns_unclassified = None
__model = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_all_columns_data() -> json:
    all_data_columns = None
    global __all_columns_unclassified
    global __model
    with open(os.path.join(BASE_DIR, "columns_without_classification.json")) as f:
        __all_columns_unclassified = json.load(f)
    with open(os.path.join(BASE_DIR, "columns.json"), 'r') as f:
        all_data_columns = json.load(f)
    with open(os.path.join(BASE_DIR, "price_prediction_model.pickle"), 'rb') as f:
        __model = pickle.load(f)
    return all_data_columns

def get_estimation_price(string_defination:dict, quantity_defination:dict):
    #get_all_columns_data()
    province_index = __all_columns_unclassified.index(string_defination['province'])
    city_index = __all_columns_unclassified.index(string_defination['city'])
    home_type = __all_columns_unclassified.index(string_defination['home_type'])
    smoking_permisstion = __all_columns_unclassified.index(string_defination['is_smoking'])

    x= np.zeros(len(__all_columns_unclassified)+7)
    x[province_index] =1
    x[city_index] =1
    x[home_type] =1
    x[smoking_permisstion] =1
    x[0] = quantity_defination['beds']
    x[1] = quantity_defination['baths']
    x[2] = quantity_defination['sq_feet']
    x[3] = quantity_defination['cats']
    x[4] = quantity_defination['dogs']
    x[5] = quantity_defination['nbr_beds']

    return round(__model.predict([x])[0], 2)


if __name__ == '__main__':
    get_all_columns_data()
    dummies_transformed = {'province':'alberta', 'city':'airdrie', 'home_type':'townhouse', 'is_smoking':'non-smoking'}
    quantified_variables = {'beds':2, 'baths':2.5, 'sq_feet':1403.0,'cats':1, 'dogs':1,'nbr_beds':2.0}
    print(get_estimation_price(dummies_transformed, quantified_variables))