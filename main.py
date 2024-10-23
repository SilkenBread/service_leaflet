from fastapi import FastAPI, HTTPException  # Framework y excepciones HTTP
from typing import Dict  # Tipado para los tipos de datos
import httpx  # Cliente HTTP asíncrono para hacer peticiones
import re  # Módulo para expresiones regulares

# Inicializa la aplicación de FastAPI
app = FastAPI()

# URL base de Nominatim para geocodificación y reverse-geocoding
NOMINATIM_URL = "https://nominatim.openstreetmap.org/"

@app.get("/geocode")
async def geocode(address: str):
    """
    Endpoint para convertir una dirección en coordenadas (latitud y longitud).
    
    Parámetros:
    - address: str -> La dirección que el usuario desea geocodificar.
    
    Retorna:
    - Un diccionario con las coordenadas latitud y longitud.
    """
    # Normaliza la dirección antes de enviarla a Nominatim
    normalized_address = normalize_address(address)

    # Parámetros de la petición HTTP a Nominatim
    params = {"q": normalized_address, "format": "json", "limit": 1}

    # Hace una petición GET asíncrona al endpoint de búsqueda de Nominatim
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NOMINATIM_URL}search", params=params)

    # Verifica si la petición fue exitosa y contiene datos
    if response.status_code != 200 or not response.json():
        # Lanza una excepción si no se encontró la dirección
        raise HTTPException(status_code=404, detail="Address not found")

    # Extrae la latitud y longitud del primer resultado
    data = response.json()[0]
    return {"lat": data["lat"], "lon": data["lon"]}


@app.get("/reverse-geocode")
async def reverse_geocode(lat: float, lon: float):
    """
    Endpoint para convertir coordenadas (latitud y longitud) en una dirección.
    
    Parámetros:
    - lat: float -> Latitud de la ubicación.
    - lon: float -> Longitud de la ubicación.
    
    Retorna:
    - Un diccionario con los detalles de la dirección aproximada.
    """
    # Parámetros de la petición HTTP para reverse-geocoding en Nominatim
    params = {"lat": lat, "lon": lon, "format": "json"}

    # Hace una petición GET asíncrona al endpoint de reverse-geocoding de Nominatim
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NOMINATIM_URL}reverse", params=params)

    # Verifica si la respuesta es válida y contiene una dirección
    if response.status_code != 200 or "address" not in response.json():
        # Lanza una excepción si no se encontraron resultados para las coordenadas
        raise HTTPException(status_code=404, detail="Coordinates not found")

    # Devuelve los detalles de la dirección obtenida
    return response.json()["address"]


def normalize_address(address: str) -> str:
    """
    Limpia y normaliza una dirección para mejorar su interpretación.
    
    Reemplazos:
    - Reemplaza '#' por 'No.'.
    - Elimina espacios adicionales o duplicados.
    
    Parámetros:
    - address: str -> La dirección ingresada por el usuario.
    
    Retorna:
    - La dirección normalizada como un string.
    """
    # Reemplaza '#' por 'No.' para evitar confusiones en la API de Nominatim
    address = re.sub(r'#', 'No.', address)

    # Elimina espacios en blanco duplicados y recorta los espacios iniciales/finales
    address = re.sub(r'\s+', ' ', address.strip())

    return address
