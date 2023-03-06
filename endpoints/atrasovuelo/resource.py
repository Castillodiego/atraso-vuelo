#Se importan que se utilizan en el codigo anterior 
import pandas as pd
import warnings
import joblib

warnings.filterwarnings('ignore')


xgboost_model=joblib.load('endpoints/atrasovuelo/XGBoost-model.joblib') 
transformer=joblib.load('endpoints/atrasovuelo/column-transformer.joblib') 

total_column=['encoder__x0_Aerolineas Argentinas',
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


def prediction(opera,mes,tipovuelo, column_transformer=transformer, model=xgboost_model, total_column_dummies=total_column):

    input_dictionnary={'OPERA':[str(opera)],'MES':[int(mes)],'TIPOVUELO':[str(tipovuelo)]}

    pd_input=pd.DataFrame.from_dict(input_dictionnary)

    transformed_data= column_transformer.fit_transform(pd_input)
    features = pd.DataFrame(transformed_data, columns=column_transformer.get_feature_names())
    features_with_missing_values=  pd.DataFrame(features, columns=total_column_dummies)

    features_with_missing_values.fillna(0)
    prediction = model.predict(features_with_missing_values)
    
   

    return prediction[0]


#print(prediction('Iberia', 3,'I'))
       
    