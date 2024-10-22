FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Copiar el archivo de dependencias y el código
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ejecutar el servidor Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8095", "--reload"]
