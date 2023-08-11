import pandas as pd
from pandas import DataFrame
import numpy as np
from pathlib import Path
from CarPredictorWS.settings import BASE_DIR
from priceForm.models import Arac
from sklearn.preprocessing import MinMaxScaler, LabelEncoder 
from .model_loader import load_car_price_model

def preprocess_data(df):
    #14. sütun
    for i in range(len(df[14])):
        if df[14][i] == "Takasa Uygun" or df[14][i] == "Belirtilmemiş" or df[14][i]=="Galeriden" or df[14][i]=='Takasa Uygun Değil' or df[14][i]=='Boya-değişen:' or df[14][i]== 'Favori' or df[14][i]=='Yetkili Bayiden' or df[14][i]=='Kimden:' or df[14][i]=='Sahibinden' or df[14][i]=='Takasa Uygun:':
            df[14][i] = None  

    #13 için int yapma ve alakası değerleri yok etme
    array = df[13].values
    def convert_to_int(value):
        try:
            return int(value.split(' ')[0])
        except:
            return None
    converted_array1 = [convert_to_int(item) for item in array]
    df[13]=converted_array1

    #12 için int yapma ve alakası değerleri yok etme
    array = df[12].values
    def convert_to_float(value):
        try:
            return float(value.replace(',', '.').split(' ')[0])
        except:
            return None

    converted_array2 = [convert_to_float(item) for item in array]
    df[12]=converted_array2    
    #İlk sütun için
    array = df[0].values
    def convert_to_float(value):
        try:
            return int(value.replace(' TL', '').replace('.', ''))
        except:
            return None
    converted_array = [convert_to_float(item) for item in array]
    df[0]=converted_array
    
    #4 sütun için
    unwanted_strings = ['6.001 km', 'Kilometre:', '248.888 km', 'Yıl:']
    df.loc[df[4].isin(unwanted_strings), 4] = None
    df[4] = pd.to_numeric(df[4], errors='coerce').astype('Int64')

    #df[5]
    array = df[5].values
    def convert_to_int(value):
        try:
            return int(value.replace(" km", "").replace(".", "").strip())
        except:
            return None

    converted_array = [convert_to_int(item) for item in array]
    df[5] = converted_array

    #df[6]
    for i in range(len(df[6])):
        if df[6][i] == 'Vites Tipi:' or df[6][i] == 'Yakıt Tipi:' or df[6][i] == 'Elektrik' or df[6][i] == 'LPG & Benzin':
            df.loc[i, 6] = None

    #df[7]
    for i in range(len(df[7])):
        if df[7][i] == 'Hatchback/5' or df[7][i] == 'Yakıt Tipi:' or df[7][i] == 'Kasa Tipi:' or df[7][i] == 'Sedan':
            df.loc[i, 7] = None        

    #df[8]
    for i in range(len(df[8])):
        if df[8][i] == 'Kasa Tipi:' or df[8][i] == '-' or df[8][i] == 'Motor Hacmi:' or df[8][i] == '1239 cc':
            df.loc[i, 8] = None    
    
    #df[9]
    unwanted_strings = ['65 hp', '2 değişen', '2501 - 3000 cm3', '2 değişen, 10 boyalı', '1 değişen','3 boyalı', '1 değişen, 3 boyalı', 'Motor Gücü:','Belirtilmemiş', 'Önden Çekiş', '1 boyalı', 'Tamamı orjinal', '2 boyalı', '-', '3001 - 3500 cm3', '4501 - 5000 cm3', '136 hp', '1601 - 1800 cm3', 'Motor Hacmi:', '1801 - 2000 cm3', '1401 - 1600 cm3','1201 - 1400 cm3' ]
    df.loc[df[9].isin(unwanted_strings), 9] = None
    array = df[9].values
    def convert_to_int(value):
        try:
            return int(value.split(' ')[0])
        except:
            return None
    converted_array = [convert_to_int(item) for item in array]
    df[9]=converted_array

    #df[10]
    replacement_values = {
        '51 - 75 HP': '63 hp',
        '151 - 175 HP': '163 hp',
        '101 - 125 HP': '113 hp',
        '176 - 200 HP': '188 hp',
        '76 - 100 HP': '88 hp',
        '426 - 450 HP': '435 hp',
        '126 - 150 HP': '138 hp',
        '601 HP ve üzeri': '610 hp',
        '301 - 325 HP': '313 hp',
        '476 - 500 HP': '488 hp',
        "50 HP'ye kadar": '50'
    }

    df[10] = df[10].replace(replacement_values)
    unwanted_strings = ['Motor Gücü:', '4WD (Sürekli)', 'Takasa Uygun', 'Takasa Uygun Değil', 'Arkadan İtiş', 'Tamamı orjinal','Çekiş:', '-' ]
    df.loc[df[10].isin(unwanted_strings), 10] = None
    array = df[10].values

    def convert_to_int(value):
        try:
            return int(value.split(' ')[0])
        except:
            return None

    converted_array = [convert_to_int(item) for item in array]
    df[10]=converted_array    

    #df[11]
    unwanted_strings = ['Çekiş:', 'Tamamı orjinal','-', 'Sahibinden', '52 lt', 'Takasa Uygun Değil','Ort. Yakıt Tüketimi:', '44 lt']
    df.loc[df[11].isin(unwanted_strings), 11] = None
    df.columns = ["Fiyat","Marka","Seri", "Model", "Yıl","Kilometre", "VitesTipi", "YakıtTipi", "KasaTipi", "MotorHacmi", "MotorGücü", "Çekiş", "OrtYakıtTüketimi", "YakıtDeposu", "BoyaDeğişen" ]

    #Cleaning DataFrame
    df.drop("BoyaDeğişen", axis=1, inplace=True)

    a=df[df["Yıl"].isnull() & df["Yıl"].isnull()& df["Kilometre"].isnull() & df["VitesTipi"].isnull() & df["YakıtTipi"].isnull() & df["KasaTipi"].isnull() & df["MotorHacmi"].isnull() & df["MotorGücü"].isnull() & df["Çekiş"].isnull() & df["OrtYakıtTüketimi"].isnull() & df["YakıtDeposu"].isnull()]
    df=df.drop(a.index)

    df["YakıtDeposu"].fillna(df["YakıtDeposu"].mean(), inplace=True)
    df["OrtYakıtTüketimi"].fillna(df["OrtYakıtTüketimi"].mean(), inplace=True)

    data=['Cabrio','Coupe','Cabrio','Cabrio','Sedan','Cabrio','Cabrio'  ]
    a=[948, 1055, 1093, 1335, 1408, 1458, 1905]
    j=0
    for i in a:
        df.at[i, "KasaTipi"]=data[j]
        j+=1

    df["Çekiş"].fillna(df["Çekiş"].mode()[0], inplace=True)
    df["MotorGücü"].fillna(df["MotorGücü"].median(), inplace= True)
    df["MotorHacmi"].fillna(df["MotorHacmi"].median(), inplace= True)
    
    return df

def main():
    csv_path = Path(BASE_DIR) / 'static' / 'car_dataset.csv'
    df = pd.read_csv(csv_path, header=None)

    preprocessed_data: DataFrame = preprocess_data(df)
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
        "OrtYakıtTüketimi": last_car.OrtYakıtTüketimi,
        "YakıtDeposu": last_car.YakıtDeposu
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

    preprocessed_data = pd.DataFrame(preprocessed_data, columns=["Marka", "Seri", "Model", "Yıl", "Kilometre", "VitesTipi", "YakıtTipi", "KasaTipi", "MotorHacmi", "MotorGücü", "Çekiş", "OrtYakıtTüketimi", "YakıtDeposu"])
    predict_edilecek_data=preprocessed_data.iloc[-1].values
    model=load_car_price_model()
    normalized_predict=model.predict([predict_edilecek_data])
    fiyat=np.concatenate((fiyat,normalized_predict))
    fiyat=scaller.inverse_transform(fiyat.reshape(-1, 1)).flatten()
    predict_value=fiyat[-1]
    return predict_value

    


    


    