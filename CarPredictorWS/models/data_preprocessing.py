import pandas as pd
from pandas import DataFrame
import numpy as np
from pathlib import Path
from CarPredictorWS.settings import BASE_DIR
from priceForm.models import Arac
from sklearn.preprocessing import MinMaxScaler, LabelEncoder 
from .model_loader import load_car_price_model

def main():
    csv_path = Path(BASE_DIR) / 'static' / 'car_dataset.csv'
    preprocessed_data = pd.read_csv(csv_path)

    fiyat=preprocessed_data["Fiyat"].values
    preprocessed_data=preprocessed_data.drop("Fiyat", axis=1)

    last_car = Arac.objects.last()
    last_car_data = {
        "Marka": last_car.Marka,
        "Seri": last_car.Seri,
        "Model": last_car.Model,
        "Yıl": last_car.Yıl,
        "Kilometre": last_car.Kilometre,
        "VitesTipi": last_car.VitesTipi,
        "YakıtTipi": last_car.YakıtTipi,
        "KasaTipi": last_car.KasaTipi,
        "MotorHacmi": last_car.MotorHacmi,
        "MotorGücü": last_car.MotorGücü,
        "Çekiş": last_car.Çekiş,
    }

    en_son_arac_df = pd.DataFrame([last_car_data])

    preprocessed_data = preprocessed_data.append(en_son_arac_df, ignore_index=True)

    #LabelEncoder
    label_encoder = LabelEncoder()
    for col in preprocessed_data.select_dtypes(include='object'):
        preprocessed_data[col] = label_encoder.fit_transform(preprocessed_data[col])
    
    scaller=MinMaxScaler()
    preprocessed_data= scaller.fit_transform(preprocessed_data)
    fiyat=fiyat.reshape(-1,1)
    fiyat=scaller.fit_transform(fiyat).flatten()

    preprocessed_data = pd.DataFrame(preprocessed_data, columns=["Marka", "Seri", "Model", "Yıl", "Kilometre", "VitesTipi", "YakıtTipi", "KasaTipi", "MotorHacmi", "MotorGücü", "Çekiş"])
    predict_edilecek_data=preprocessed_data.iloc[-1].values
    model=load_car_price_model()
    normalized_predict=model.predict([predict_edilecek_data])
    fiyat=np.concatenate((fiyat,normalized_predict))
    fiyat=scaller.inverse_transform(fiyat.reshape(-1, 1)).flatten()
    predict_value=fiyat[-1]
    return predict_value

    


    


    