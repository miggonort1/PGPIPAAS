# Usar una imagen base oficial de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /proyecto

# Instalar dependencias del sistema necesarias para MariaDB y herramientas de compilación
RUN apt-get update && apt-get install -y \
    pkg-config \
    mariadb-server \
    libmariadb-dev \
    build-essential \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Descargar wait-for-it para esperar a que los servicios estén listos
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Copiar los archivos de la aplicación al contenedor
# Esto incluye requirements.txt
COPY . .

# Instalar las dependencias de Python
# Usamos una ruta relativa porque el WORKDIR ya es /proyecto
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install stripe python-decouple

# Crear un script SQL para inicialización de la base de datos
COPY setup.sql /docker-entrypoint-initdb.d/

# Copiar y asignar permisos al script de entrada
COPY entrypoint.sh /usr/local/bin/
RUN dos2unix /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Exponer los puertos necesarios
EXPOSE 3306 8000

# Configurar el script de entrada como comando por defecto
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
