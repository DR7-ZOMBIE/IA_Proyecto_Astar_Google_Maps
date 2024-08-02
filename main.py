import pandas as pd
import matplotlib.pyplot as plt
import osmnx as ox
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
from collections import defaultdict
from AlexAi import Node, Tree  # Importar las clases Node y Tree
import json

ox.config(use_cache=True, log_console=True)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las orígenes, cambiar según necesidad
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)


class Intersection(Node):
    # Cargar JSON desde un archivo
    with open('final_df.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    def __init__(self, state, adjacents, node_coords, end_node, operators=[], operator=None, parent=None, objective=None):
        # Asegúrate de pasar los parámetros iniciales a la clase base
        super().__init__(state, operators, operator=operator, parent=parent, objective=objective)

        self.adjacents = adjacents
        self.node_coords = node_coords
        self.end_node = end_node
        self.vel_acum = 0 if parent is None else parent.vel_acum + self.velocity()

    def getchildrens(self):
        return [state if not self.repeatStatePath(state) else None for state in self.adjacents.get(self.state, [])]

    def get_promedio_vel_acum(self):
        return self.vel_acum / self.level if self.level != 0 else 0

    def heuristic(self):
        if self.state == self.end_node:
            return 0
        else:
            return self.node_coords[self.state].distance(self.node_coords[self.end_node]) * 100000 / (self.get_promedio_vel_acum() if self.get_promedio_vel_acum() != 0 else 1)

    def velocity(self):
        if self.parent is None:
            return 0
        u = str(self.parent.state)
        v = str(self.state)
        return self.data[u][v]['velocidad'] if v in self.data[u] else 0

    def cost(self):
        if self.parent is None:
            return 0
        u = str(self.parent.state)
        v = str(self.state)
        return self.data[u][v]['peso'] if v in self.data[u] else 0

    

# Definir el modelo de datos para la solicitud

class MapRequest(BaseModel):
    city_selected: str
    init_node: dict
    final_node: dict

# Función para construir el grafo y las estructuras de datos


def build_graph(city, transport_mode='drive'):
    G = ox.graph_from_place(city, network_type=transport_mode, simplify=True)
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    
    adjacents = defaultdict(list)
    for u, v, k in gdf_edges.index:
        adjacents[u].append(v)
    adjacents = dict(adjacents)

    node_coords = {node: data['geometry']
                   for node, data in gdf_nodes.to_dict('index').items()}
    return G, adjacents, node_coords


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Endpoint para renderizar el mapa


@app.get("/render_map")
async def render_map(city: str = 'Envigado, Antioquia, Colombia', transport_mode: str = 'drive'):
    G, adjacents, node_coords = build_graph(city, transport_mode)
    try:
        start_node = ox.nearest_nodes(G, Y=start_lat, X=start_lon)
        end_node = ox.nearest_nodes(G, Y=end_lat, X=end_lon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    class Intersection(Node):
        def getchildrens(self):
            return [
                state
                if not self.repeatStatePath(state)
                else None for state in adjacents.get(self.state, [])
            ]

        def cost(self):
            if self.parent is None:
                return 0
            return node_coords[self.state].distance(node_coords[self.parent.state]) * 100000

        def heuristic(self):
            if self.state == end_node:
                return 0
            else:
                return node_coords[self.state].distance(node_coords[end_node]) * 100000

    MapaTree = Tree(Intersection(state=start_node,
                    operators=[], objective=end_node))
    objective = MapaTree.aAsterisk(endState=end_node)
    path_nodes = MapaTree.pathStates()

    if not path_nodes or any(node not in G for node in path_nodes):
        raise HTTPException(status_code=404, detail="Route not found")

    # Generar el mapa con la ruta
    try:
        fig, ax = ox.plot_graph_route(
            G, path_nodes, route_linewidth=6, node_size=0, bgcolor='k', show=False, close=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# Endpoint para recibir JSON y renderizar el mapa


@app.post("/render_map_with_data")
async def render_map_with_data(data: MapRequest = Body(...)):
    city = data.city_selected
    start_lat = data.init_node['lat']
    start_lon = data.init_node['lon']
    end_lat = data.final_node['lat']
    end_lon = data.final_node['lon']

    G, adjacents, node_coords = build_graph(city)
    try:
        start_node = ox.nearest_nodes(G, Y=start_lat, X=start_lon)
        end_node = ox.nearest_nodes(G, Y=end_lat, X=end_lon)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    MapaTree = Tree(Intersection(state=start_node, adjacents=adjacents, node_coords=node_coords, end_node=end_node, objective=end_node))
    MapaTree.aAsterisk(endState=end_node)
    path_nodes = MapaTree.pathStates()

    if not path_nodes:
        raise HTTPException(status_code=404, detail="Route not found")

    try:
        fig, ax = ox.plot_graph_route(
            G, path_nodes, route_linewidth=6, node_size=0, bgcolor='k', show=False, close=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

