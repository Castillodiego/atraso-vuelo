#Se importan que se utilizan en el codigo anterior 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import missingno as msng
import warnings

from datetime import datetime

warnings.filterwarnings('ignore')


from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report


#se lee el dataset
df = pd.read_csv('dataset_SCL.csv')

def dif_min(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    dif_min = ((fecha_o - fecha_i).total_seconds())/60
    return dif_min
        
df['dif_min'] = df.apply(dif_min, axis = 1)

df['atraso_15'] = np.where(df['dif_min'] > 15, 1, 0)
data = shuffle(df[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'atraso_15']], random_state = 111)
features = pd.concat([pd.get_dummies(data['OPERA'], prefix = 'OPERA'),pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), pd.get_dummies(data['MES'], prefix = 'MES')], axis = 1)


label = data['atraso_15']

x_train, x_test, y_train, y_test = train_test_split(features, label, test_size = 0.33, random_state = 42)

logReg = LogisticRegression()
model = logReg.fit(x_train, y_train)

y_pred = model.predict(x_test)

print(y_pred)