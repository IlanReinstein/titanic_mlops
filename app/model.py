import pickle
from app.preprocessing import prepare_data

with open('models/titanic_rf.pkl', 'rb') as f:
    model = pickle.load(f)


def predict_single(features):
    preprocessed_features = prepare_data(features)
    return model.predict([preprocessed_features])[0]


def predict_batch(instances):
    preprocessed_instances = prepare_data(instances)
    return model.predict(preprocessed_instances).tolist()
