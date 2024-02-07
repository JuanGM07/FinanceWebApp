import pandas as pd  
from datetime import datetime
import json
import requests
import streamlit as st


def run_av_etl(symbol):
    # URL base para obtener el Monthly Adjusted Time Series
    API_KEY = '8YU0716207LE5V4X'
    base_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}'
 
    # Reemplaza 'TU_API_KEY' y 'AAPL' con tu clave de API y el símbolo de la empresa respectivamente
    try:
        # Realizar la solicitud GET a la API de Alpha Vantage
        response = requests.get(base_url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar si 'Monthly Adjusted Time Series' está presente en los datos
            if 'Monthly Adjusted Time Series' in data:
                # Crear un DataFrame a partir de los datos
                df = pd.DataFrame(data['Monthly Adjusted Time Series']).T
                
                # Cambiar el índice a formato de fecha
                df.index = pd.to_datetime(df.index)
                
                # Ordenar cronológicamente descendente
                df = df.sort_index(ascending=False)
                
                # Mostrar los primeros registros del DataFrame
                print(df.head())
            else:
                print("No se encontraron datos mensuales ajustados para este símbolo.")
        else:
            print("La solicitud no fue exitosa. Código de estado:", response.status_code)

    except requests.RequestException as e:
        print("Error al realizar la solicitud:", e)

    return df

    





