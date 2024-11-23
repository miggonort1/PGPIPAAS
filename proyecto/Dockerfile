# Usar una imagen oficial de Python 3.12
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /proyecto

# Copiar el contenido del directorio actual al contenedor
COPY . /proyecto

# Instalar las dependencias
RUN pip install --no-cache-dir -r proyecto/requirements.txt

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
