FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libblas3 \
    liblapack3 \
    libatlas-base-dev \
    gfortran \
    netcat-openbsd \
    dos2unix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar y preparar el script wait-for-it.sh
COPY wait-for-it.sh /app/wait-for-it.sh
RUN dos2unix /app/wait-for-it.sh && chmod +x /app/wait-for-it.sh

# Copiar e instalar las dependencias del proyecto
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . /app/

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8002"]
