import joblib

import traceback
import pandas as pd
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from preprocessing import prepare_data


# Your API definition
app = Flask(__name__)



DATABASE_URL = "sqlite:///./predictions.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Create the database tables
Base.metadata.create_all(bind=engine)


# @app.route('/')
# def home():
#     return "API is working!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_ = request.get_json(force=True)
        # print(request)
        # print(json_)
        in_dat = pd.DataFrame.from_dict(json_)
        # prepare data for predictions
        features_df = prepare_data(in_dat).drop(columns='PassengerId')
        predictions = model.predict(features_df)
        # create empty dataframe for return
        out_df = pd.DataFrame(in_dat['PassengerId'])
        out_df['Survived'] = predictions

        return out_df.to_json(orient='records')
        # return jsonify({'input': json_})

    except:

        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    # Load "model.pkl"

    model = joblib.load('models/titanic_rf.pkl')
    print('Model loaded')
    app.run(debug=True, port=8000, host='0.0.0.0')
