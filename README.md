# Servicio GeoCoding - FastAPI ⚡

### Iniciar proyecto con Docker
```bash
docker build -t fastapi-leaflet .
```

```bash
docker run -d -p 8095:8095 fastapi-leaflet
```

### Uso API Geocode
Request:
```
http://localhost:8095/geocode?address=Plaza de Bolívar, Bogotá
```
Response:
```
{
  "lat": "4.598146",
  "lon": "-74.07600427912425"
}
```

### Uso API Reverse Geocode
Request:
```
http://localhost:8095/reverse-geocode?lat=4.5980478&lon=-74.0760866
```
Response:
```
{
  "road": "Calle 17",
  "neighbourhood": "UPZs de Bogotá",
  "suburb": "Localidad Santa Fé",
  "city": "Bogotá",
  "region": "RAP (Especial) Central",
  "postcode": "110321",
  "country": "Colombia",
  "country_code": "co"
}
```
