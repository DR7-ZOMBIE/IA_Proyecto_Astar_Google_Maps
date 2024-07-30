import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

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
        'annotations': 'duration,speed,congestion'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data:
        congestion_levels = data['routes'][0]['legs'][0]['annotation']['congestion']
        # se considera el valor más frecuente en la lista de congestiones
        congestion = max(set(congestion_levels), key=congestion_levels.count)
        duration = data['routes'][0]['duration']  # en segundos
        speed = data['routes'][0]['legs'][0]['annotation']['speed'][0]  # en metros por segundo
        print(f"Processed {row['index']}")
        return row['index'], duration, speed, congestion
    else:
        print(f"Failed to process {row['index']}")
        return row['index'], None, None, None

# Procesar los datos
def process_data(data, modality):
    data['u_coords'], data['v_coords'] = zip(*data['geometry'].apply(extract_coordinates))
    data = data.reset_index()
    durations = [None] * len(data)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_traffic_info, row) for _, row in data.iterrows()]
        for future in futures:
            index, duration, speed, congestion_response  = future.result()
            durations[index] = duration
    
    final_data = data[['u', 'v', 'geometry']].copy()
    final_data['duration_s'] = durations
    final_data['time_car'] = final_data['duration_s'] / 60  # Convertir segundos a minutos
    return final_data

# Cargar datos
data = pd.read_csv('gdf_edges.csv')

# Ejecutar procesamiento
final_df = process_data(data, 'driving')

final_df.to_csv('final_df.csv', index=False)
print(final_df.head())