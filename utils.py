import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Funcion para sacar un promedio en las columnas que tienen un array de velocidades
def parse_maxspeed(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, str) and '[' in x:
        speeds = eval(x)
        speeds = [float(speed) for speed in speeds]
        return sum(speeds) / len(speeds)
    elif isinstance(x, str):
        return float(x)
    return x  

# Extrae las coordenadas de los puntos u y v que estan en la columna geometry
def extract_coordinates(linestring):
    #se parte el string en dos puntos y luego se crea la columna u_coords y v_coords que son las coordendas de c/u
    points = linestring.replace('LINESTRING (', '').replace(')', '').split(', ')
    u_coords = tuple(map(float, points[0].split()))
    v_coords = tuple(map(float, points[-1].split()))
    return u_coords, v_coords

def calculate_speed(data: pd.DataFrame):
    # Se calcula la velocidad promedio de cada camino y se llena con 45 si no hay informacion
    data['speed_kph'] = data['maxspeed'].apply(parse_maxspeed)
    data['speed_kph'].fillna(45, inplace=True)
    # Transformacion de speed_kph a metros x segundo (aquí se asume que las motos viajan 20% más rápido que los carros)
    data['time_car'] = data['distance_m'] / (data['speed_kph'] * 1000 / 60)  # tiempo en minutos
    data['time_motorcycle'] = data['distance_m'] / (data['speed_kph'] * 1.2 * 1000 / 60) 
    return data

#Función para reducir decimales
def reduce_decimals(data: pd.DataFrame):
    data['distance_m'] = data['distance_m'].apply(lambda x: (round(x, 4)))
    data['time_car'] = data['time_car'].apply(lambda x: (round(x, 5)))
    data['time_motorcycle'] = data['time_motorcycle'].apply(lambda x: (round(x, 5)))
    return data

def process_geometry(data: pd.DataFrame):
    # Se extraen las coordenadas de los puntos u y v y se calcula la distancia entre ellos utilizando geodesic
    data['u_coords'], data['v_coords'] = zip(*data['geometry'].apply(extract_coordinates))
    data['distance_m'] = data.apply(lambda row: geodesic(row['u_coords'], row['v_coords']).meters, axis=1)
    data = calculate_speed(data)
    final_df = data[['u', 'v', 'u_coords', 'v_coords', 'distance_m','time_car', 'time_motorcycle']]
    final_df = reduce_decimals(final_df)
    return final_df


