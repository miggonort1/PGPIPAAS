#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Esperar a que la base de datos esté lista
echo "Esperando a que la base de datos esté lista..."
/usr/local/bin/wait-for-it $DB_HOST:$DB_PORT -- echo "Base de datos disponible."

# Realizar migraciones de Django
echo "Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar el servidor de desarrollo de Django
echo "Iniciando el servidor..."
exec python manage.py runserver 0.0.0.0:8000
