# 🌍 Proyecto de Rutas con FastAPI

Este proyecto utiliza **FastAPI** para crear una API que permite calcular y visualizar rutas en un mapa. Se basa en datos de **OpenStreetMap** y utiliza técnicas de búsqueda de caminos para encontrar la mejor ruta entre dos puntos.

---

## 📑 Tabla de Contenidos

1. [Requisitos](#-requisitos)
2. [Instalación](#️-instalación)
3. [Estructura del Proyecto](#-estructura-del-proyecto)
4. [Uso](#-uso)
   - [Ejecutar el Servidor](#ejecutar-el-servidor)
   - [Endpoints](#endpoints)
   - [Ejemplo de Uso](#ejemplo-de-uso)
5. [Notas](#-notas)
6. [Contribuciones](#-contribuciones)
7. [Licencia](#-licencia)

---

## 📋 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener **Python 3.7** o superior instalado en tu sistema.

---

## ⚙️ Instalación

### Clona el repositorio (si aún no lo has hecho):

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
Crea y activa un entorno virtual:
bash
Copiar código
python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`
Instala las dependencias:
bash
Copiar código
pip install fastapi uvicorn pydot ipython pandas matplotlib osmnx pydantic aiohttp requests graphviz
📁 Estructura del Proyecto
El proyecto tiene la siguiente estructura:

main.py: El archivo principal que contiene la implementación de FastAPI.
AlexAi.py: Define las clases Node y Tree utilizadas para el algoritmo de búsqueda de caminos.
final_df.json: Archivo JSON con datos necesarios para las operaciones (cargado en el código).
🚀 Uso
Ejecutar el Servidor
Para ejecutar el servidor FastAPI, usa el siguiente comando:

bash
Copiar código
uvicorn main:app --reload
Esto iniciará el servidor en http://127.0.0.1:8000 con recarga automática durante el desarrollo.

Endpoints
GET /
Descripción: Endpoint de prueba que devuelve un mensaje de bienvenida.

Respuesta:

json
Copiar código
{
  "message": "Hello World"
}
GET /render_map
Descripción: Renderiza un mapa de la ciudad especificada con la ruta calculada entre dos puntos.
Parámetros:
city (opcional): Ciudad para la cual se debe renderizar el mapa (por defecto 'Envigado, Antioquia, Colombia').
transport_mode (opcional): Modo de transporte para el cálculo de rutas (por defecto 'drive').
Respuesta: Imagen PNG del mapa con la ruta.
POST /render_map_with_data
Descripción: Renderiza un mapa utilizando datos proporcionados en el cuerpo de la solicitud.

Cuerpo de la Solicitud:

json
Copiar código
{
  "city_selected": "Nombre de la Ciudad",
  "init_node": {"lat": <latitud_inicial>, "lon": <longitud_inicial>},
  "final_node": {"lat": <latitud_final>, "lon": <longitud_final>}
}
Respuesta: Imagen PNG del mapa con la ruta.

Ejemplo de Uso
Para probar el endpoint /render_map_with_data, puedes usar curl o herramientas como Postman para enviar una solicitud POST con los datos requeridos.

Ejemplo con curl:

bash
Copiar código
curl -X POST "http://127.0.0.1:8000/render_map_with_data" -H "Content-Type: application/json" -d '{
  "city_selected": "Envigado, Antioquia, Colombia",
  "init_node": {"lat": 6.1675, "lon": -75.5976},
  "final_node": {"lat": 6.1690, "lon": -75.5950}
}'
📝 Notas
Asegúrate de que final_df.json esté presente en el directorio raíz del proyecto para que el código funcione correctamente.
Si encuentras algún error, revisa los registros del servidor para obtener más detalles.
🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un problema o envía una solicitud de extracción para discutir cambios o mejoras.

📄 Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

markdown
Copiar código

### Key Features:
- **Headings and Emojis:** For section titles to make them stand out and engage the reader.
- **Code Blocks:** For commands and JSON snippets to improve clarity and readability.
- **Table of Contents:** Quick navigation to various sections.
- **Section Separators:** Horizontal lines to distinguish different sections and improve readability.
- **Detailed Instructions:** Clear step-by-step guide for setup, usage, and contribution.

You can replace `<URL_DEL_REPOSITORIO>` and `<NOMBRE_DEL_REPOSITORIO>` with the actual URL 
