#!/bin/sh

# Iniciar MariaDB en segundo plano
mysqld_safe --skip-networking &
MARIADB_PID=$!

# Esperar a que MariaDB esté listo
echo "Esperando a que MariaDB esté listo..."
while ! mysqladmin ping --silent; do
    sleep 1
done
echo "MariaDB está listo."

# Iniciar el servidor de Django
wait-for-it localhost:3306 -- python manage.py runserver 0.0.0.0:8000

# Esperar a que MariaDB termine (cuando se detenga el contenedor)
wait $MARIADB_PID
