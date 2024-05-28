"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.5
"""
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_hearth_data(health: pd.DataFrame) -> pd.DataFrame:

    label_encoder = LabelEncoder()
    health["HeartDisease"] = label_encoder.fit_transform(health["HeartDisease"])
    health["Smoking"] = label_encoder.fit_transform(health["Smoking"])
    health["AlcoholDrinking"] = label_encoder.fit_transform(health["AlcoholDrinking"])
    health["Stroke"] = label_encoder.fit_transform(health["Stroke"])
    health["DiffWalking"] = label_encoder.fit_transform(health["DiffWalking"])
    health["Sex"] = label_encoder.fit_transform(health["Sex"])
    health["AgeCategory"] = label_encoder.fit_transform(health["AgeCategory"])
    health["Race"] = label_encoder.fit_transform(health["Race"])
    health["Diabetic"] = label_encoder.fit_transform(health["Diabetic"])
    health["PhysicalActivity"] = label_encoder.fit_transform(health["PhysicalActivity"])
    health["Asthma"] = label_encoder.fit_transform(health["Asthma"])
    health["KidneyDisease"] = label_encoder.fit_transform(health["KidneyDisease"])
    health["SkinCancer"] = label_encoder.fit_transform(health["SkinCancer"])
    health["GenHealth"] = label_encoder.fit_transform(health["GenHealth"])

    #tutaj jeszcze kodzik który usuwa wartości odstające z kolumny SleepTime

    return health
