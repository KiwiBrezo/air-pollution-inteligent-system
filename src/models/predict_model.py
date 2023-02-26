import os.path
import pickle

file_location = os.path.dirname(__file__)
model = None


def load_model():
    print("--- Starting loading model ---")
    pkl_filename = os.path.join(file_location, "../../models/modelAirPollution.pkl")
    with open(pkl_filename, 'rb') as file:
        loaded_model = pickle.load(file)

    print("--- Done loading model ---")

    return loaded_model


def predict_air_pollution(data):
    global model

    if model is None:
        print("No model is loaded, need to load model...")
        model = load_model()

    # return model.predict()
    return data
