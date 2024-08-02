import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import json
# Token de acceso a Mapbox
ACCESS_TOKEN = 'pk.eyJ1Ijoic2thaXBlMTIiLCJhIjoiY2x6NG1mc3UzM3M5bTJxcHMzYjY3OTNmbyJ9.ibafE9lySvin491TdmbkhA'

# Extraer coordenadas de los puntos u y v
def extract_coordinates(linestring):
    points = linestring.replace('LINESTRING (', '').replace(')', '').split(', ')
    u_coords = tuple(map(float, points[0].split()))
    v_coords = tuple(map(float, points[-1].split()))
    return u_coords, v_coords

# Llamar a la API de Mapbox para obtener distancia y tiempo
def get_traffic_info(row):
    u_coords = row['u_coords']
    v_coords = row['v_coords']
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving-traffic/{u_coords[0]},{u_coords[1]};{v_coords[0]},{v_coords[1]}"
    params = {
        'access_token': ACCESS_TOKEN,
        'geometries': 'geojson',
        'overview': 'full',
        'annotations': 'speed'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data:
        #speed va a ser el promedio de las velocidades del array que entrega la API
        speed = data['routes'][0]['legs'][0]['annotation']['speed']
        speed = sum(speed) / len(speed)
        weight = data['routes'][0]['legs'][0].get('weight', None)
        print(f"Processed {row['index']}")
        return row['index'], speed, weight
    else:
        print(f"Failed to process {row['index']}")
        return row['index'], None, None, None

# Procesar los datos
def process_data(data, modality):
    data['u_coords'], data['v_coords'] = zip(*data['geometry'].apply(extract_coordinates))
    data = data.reset_index()
    speeds = [None] * len(data)
    weigths = [None] * len(data)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_traffic_info, row) for _, row in data.iterrows()]
        for future in futures:
            index, speed, weigth  = future.result()
            speeds[index] = speed
            weigths[index] = weigth
    
    final_data = data[['u', 'v', 'geometry']].copy()
    final_data['speed_mps'] = speeds
    final_data['weigth'] = weigths
    return final_data

# Ejecutar procesamiento
#final_df = process_data(data, 'driving')

# Convertir el dataframe a JSON con la estructura específica
def dataframe_to_json(df):
    json_df = {row['u']: {row['v']: {"velocidad": row['speed_mps'], "peso": row['weigth']}} for index, row in df.iterrows()}
    return json_df

# Uso de la función con final_df
json_df = dataframe_to_json(final_df)
#descarga el json
with open('final_df.json', 'w') as f:
    json.dump(json_df, f)

