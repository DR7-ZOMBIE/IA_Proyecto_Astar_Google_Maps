# Proyecto de Enrutamiento con FastAPI y OSMnx

![Build Status](https://img.shields.io/travis/USER/REPO.svg)
![Coverage Status](https://coveralls.io/repos/github/USER/REPO/badge.svg)
![Version](https://img.shields.io/github/v/release/USER/REPO)
![License](https://img.shields.io/github/license/USER/REPO)

## Descripción

Este proyecto implementa una API para renderizar mapas y calcular rutas utilizando FastAPI, OSMnx, y algoritmos de búsqueda A*. La API permite la creación y consulta de rutas optimizadas entre dos puntos en una ciudad seleccionada, utilizando diversos modos de transporte.

## Funcionalidades

- Renderizar mapas de ciudades utilizando OpenStreetMap.
- Calcular rutas óptimas entre dos puntos usando el algoritmo A*.
- Soporte para diferentes modos de transporte (peatonal, en bicicleta, en coche, etc).
- Endpoints para recibir parámetros vía URL o JSON y devolver imágenes de los mapas con las rutas calculadas.

## Instalación

### Requisitos

- Python 3.8+
- FastAPI
- OSMnx
- GeoPandas
- Matplotlib
- Uvicorn

### Pasos de Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/DR7-ZOMBIE/IA_Proyecto_Astar_Google_Maps.git
    cd IA_Proyecto_Astar_Google_Maps
    ```

2. Crea un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Ejecuta la aplicación:

    ```bash
    uvicorn main:app --reload
    ```

## Uso

### Endpoints

#### `GET /render_map`

Renderiza un mapa con la ruta calculada entre dos puntos.

- **Parámetros**:
    - `city` (str): Nombre de la ciudad.
    - `transport_mode` (str): Modo de transporte (e.g., 'walk', 'bike', 'drive').
    - `start_lat` (float): Latitud del punto de inicio.
    - `start_lon` (float): Longitud del punto de inicio.
    - `end_lat` (float): Latitud del punto final.
    - `end_lon` (float): Longitud del punto final.

- **Ejemplo**:

    ```bash
    curl -X 'GET' \
      'http://127.0.0.1:8000/render_map?city=Manhattan, New York, USA&transport_mode=drive&start_lat=40.748817&start_lon=-73.985428&end_lat=40.730610&end_lon=-73.935242' \
      -H 'accept: application/json'
    ```

#### `POST /render_map_with_data`

Renderiza un mapa con la ruta calculada entre dos puntos, recibiendo los parámetros en un JSON.

- **Cuerpo de la solicitud**:

    ```json
    {
      "city_selected": "Manhattan, New York, USA",
      "transport_mode_selected": "drive",
      "init_node": {
        "lat": 40.748817,
        "lon": -73.985428
      },
      "final_node": {
        "lat": 40.730610,
        "lon": -73.935242
      }
    }
    ```

- **Ejemplo**:

    ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/render_map_with_data' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
            "city_selected": "Manhattan, New York, USA",
            "transport_mode_selected": "drive",
            "init_node": {"lat": 40.748817, "lon": -73.985428},
            "final_node": {"lat": 40.730610, "lon": -73.935242}
          }'
    ```

## Contribuir

¡Las contribuciones son bienvenidas! Por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature-nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature-nueva-funcionalidad`).
5. Crea un nuevo Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT. Mira el archivo [LICENSE](LICENSE) para más detalles.
