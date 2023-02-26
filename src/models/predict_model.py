import pickle

model = None


def load_model():
    pkl_filename = "../../models/modelAirPollution.pkl"
    with open(pkl_filename, 'rb') as file:
        loaded_model = pickle.load(file)

    return loaded_model


def predict_air_pollution(data):
    global model

    if model is None:
        model = load_model()

    # return model.predict()
    return data
