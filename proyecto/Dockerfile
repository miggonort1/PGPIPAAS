# Usar una imagen base oficial de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /proyecto

# Instalar las dependencias del sistema necesarias para mysqlclient y herramientas de compilación
RUN apt-get update && apt-get install -y \
    pkg-config \
    mariadb-server \
    mariadb-client \
    libmariadb-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Descargar wait-for-it para esperar a que la base de datos esté lista
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Copiar los archivos de la aplicación al contenedor
COPY . /proyecto

# Crear un script SQL para configuraciones iniciales
COPY setup.sql /docker-entrypoint-initdb.d/

# Copiar y asignar permisos al script de entrada
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r /proyecto/requirements.txt

# Exponer el puerto 8000
EXPOSE 3306 8000

# Comando para ejecutar el servidor de desarrollo de Django
# CMD ["sh", "-c", "wait-for-it localhost:3306 -- python manage.py runserver 0.0.0.0:8000"]

# Configurar el script de entrada como comando por defecto
ENTRYPOINT ["entrypoint.sh"]