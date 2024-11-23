# Usar una imagen base oficial de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /proyecto

# Instalar las dependencias del sistema necesarias para mysqlclient y herramientas de compilación
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de la aplicación al contenedor
COPY . /proyecto

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r /proyecto/requirements.txt

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

