import joblib

def load_car_price_model():
    model_filename = 'models/car_price_model.joblib'
    model = joblib.load(model_filename)
    return model
