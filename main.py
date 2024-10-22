from fastapi import FastAPI, HTTPException
from typing import Dict
import httpx, re

app = FastAPI()

# Nominatim endpoint for geocoding and reverse geocoding
NOMINATIM_URL = "https://nominatim.openstreetmap.org/"

@app.get("/geocode")
async def geocode(address: str):
    """API to convert an address to latitude and longitude."""
    normalized_address = normalize_address(address)
    params = {"q": normalized_address, "format": "json", "limit": 1}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NOMINATIM_URL}search", params=params)
    if response.status_code != 200 or not response.json():
        raise HTTPException(status_code=404, detail="Address not found")
    data = response.json()[0]
    return {"lat": data["lat"], "lon": data["lon"]}


@app.get("/reverse-geocode")
async def reverse_geocode(lat: float, lon: float):
    """API to convert latitude and longitude to an address."""
    params = {"lat": lat, "lon": lon, "format": "json"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NOMINATIM_URL}reverse", params=params)
    if response.status_code != 200 or "address" not in response.json():
        raise HTTPException(status_code=404, detail="Coordinates not found")
    return response.json()["address"]

def normalize_address(address: str) -> str:
    """Limpia la dirección para mejorar la interpretación."""
    # Reemplaza "#" por "No." y elimina espacios adicionales
    address = re.sub(r'#', 'No.', address)
    address = re.sub(r'\s+', ' ', address.strip())
    return address
