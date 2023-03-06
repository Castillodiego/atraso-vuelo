#Se importan que se utilizan en el codigo anterior 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msng
import warnings
from datetime import datetime
import joblib

warnings.filterwarnings('ignore')


from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report


#se lee el dataset
df = pd.read_csv('dataset_SCL.csv')

xgboost_model=joblib.load('XGBoost-model.joblib') 
transformer=joblib.load('column-transformer.joblib') 

def create_dictionnary(opera, mes, tipovuelo):
    return {'OPERA':[opera],'MES':[int(mes)],'TIPOVUELO':[tipovuelo]}

def pre_process(input_dictionary, column_transformer=transformer, model=xgboost_model):

    dic={'OPERA':['Grupo LATAM'],'MES':[5],'TIPOVUELO':['I']}

    pd_input=pd.DataFrame.from_dict(dic)
    total_column_dummies=['encoder__x0_Aerolineas Argentinas',
    'encoder__x0_Aeromexico',
 'encoder__x0_Air Canada',
 'encoder__x0_Air France',
 'encoder__x0_Alitalia',
 'encoder__x0_American Airlines',
 'encoder__x0_Austral',
 'encoder__x0_Avianca',
 'encoder__x0_British Airways',
 'encoder__x0_Copa Air',
 'encoder__x0_Delta Air',
 'encoder__x0_Gol Trans',
 'encoder__x0_Grupo LATAM',
 'encoder__x0_Iberia',
 'encoder__x0_JetSmart SPA',
 'encoder__x0_K.L.M.',
 'encoder__x0_Lacsa',
 'encoder__x0_Latin American Wings',
 'encoder__x0_Oceanair Linhas Aereas',
 'encoder__x0_Plus Ultra Lineas Aereas',
 'encoder__x0_Qantas Airways',
 'encoder__x0_Sky Airline',
 'encoder__x0_United Airlines',
 'encoder__x1_1',
 'encoder__x1_2',
 'encoder__x1_3',
 'encoder__x1_4',
 'encoder__x1_5',
 'encoder__x1_6',
 'encoder__x1_7',
 'encoder__x1_8',
 'encoder__x1_9',
 'encoder__x1_10',
 'encoder__x1_11',
 'encoder__x1_12',
 'encoder__x2_I',
 'encoder__x2_N']


    transformed_data= column_transformer.fit_transform(pd_input)
    features = pd.DataFrame(transformed_data, columns=column_transformer.get_feature_names())
    features_with_missing_values=  pd.DataFrame(features, columns=total_column_dummies)

    features_with_missing_values.fillna(0)


    prediction = model.predict(features_with_missing_values)

    return prediction

       
    