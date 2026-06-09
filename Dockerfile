# Usamos una imagen oficial y ligera de Python
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1
# Evitar que Python haga buffer de la salida (útil para ver logs en tiempo real)
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias (por ejemplo, para compilar psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalarlos
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto del código del proyecto
COPY . /app/

# Exponer el puerto por el que escuchará Gunicorn
EXPOSE 8000

# Comando por defecto al ejecutar el contenedor
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "comuniapp.wsgi:application"]
