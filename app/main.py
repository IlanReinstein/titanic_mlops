import joblib

import traceback
import pandas as pd
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from preprocessing import prepare_data

# Your API definition
app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Prediction(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # feature1 = db.Column(db.Float, nullable=False)
    # feature2 = db.Column(db.Float, nullable=False)
    # processed_feature1 = db.Column(db.Float, nullable=False)
    # processed_feature2 = db.Column(db.Float, nullable=False)
    passenger_id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Float, nullable=True)

# Initialize the database
with app.app_context():
    db.create_all()


@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_ = request.get_json(force=True)
        # print(request)
        # print(json_)
        in_dat = pd.DataFrame.from_dict(json_)
        # prepare data for predictions
        features_df = prepare_data(in_dat)
        predictions = model.predict(features_df.drop(columns='PassengerId'))
        # create empty dataframe for return
        out_df = pd.DataFrame(in_dat['PassengerId'])
        out_df['Survived'] = predictions

        # Save each record and prediction to the database
        for i, row in out_df.iterrows():
            print(row['PassengerId'])
            new_prediction = Prediction(
                passenger_id=int(row['PassengerId']),
                # feature2=features_df.iloc[i]['feature2'],
                # processed_feature1=features_df.iloc[i]['processed_feature1'],
                # processed_feature2=features_df.iloc[i]['processed_feature2'],
                result=predictions[i]
            )
            db.session.merge(new_prediction)

        # Commit all records to the database
        db.session.commit()
        return out_df.to_json(orient='records')
        # return jsonify({'input': json_})


    except Exception as e:

        return jsonify({'trace': str(e)})


if __name__ == '__main__':
    # Load "model.pkl"

    model = joblib.load('models/titanic_rf.pkl')
    print('Model loaded')
    app.run(debug=True, port=8000, host='0.0.0.0')
