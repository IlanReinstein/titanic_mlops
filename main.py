import sys
import pickle
import pandas as pd
import traceback
import numpy as np
from flask import Flask, request, jsonify
from app.preprocessing import prepare_data

# Your API definition
app = Flask(__name__)


def predict():
    try:
        json_ = request.json
        print(json_)
        in_dat = pd.DataFrame(json_)
        features_df = prepare_data(in_dat).drop(columns='PassengerId')
        preds = model.predict(features_df)
        out_dict = {
            "PassengerId": in_dat["PassengerId"],
            "Survived": preds
        }

        return jsonify({'prediction': preds})

    except:

        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])  # This is for a command-line input
    except:
        port = 5000  # If you don't provide any port the port will be set to 12345

    # Load "model.pkl"
    with open('models/titanic_rf.pkl', 'rb') as f:
        model = pickle.load(f)
    print('Model loaded')

    app.run(port=port, debug=True)
