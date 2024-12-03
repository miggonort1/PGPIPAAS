#!/bin/sh

# Configurar persistencia de datos para MariaDB
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Inicializando la base de datos de MariaDB..."
    mysql_install_db --user=mysql --datadir=/var/lib/mysql
    echo "Base de datos inicializada."
fi

# Iniciar MariaDB en segundo plano
mysqld_safe --datadir=/var/lib/mysql &
MARIADB_PID=$!

# Esperar a que MariaDB esté listo
echo "Esperando a que MariaDB esté listo..."
while ! mysqladmin ping --silent; do
    sleep 1
done
echo "MariaDB está listo."

# Ejecutar el script de inicialización SQL
if [ -f /docker-entrypoint-initdb.d/setup.sql ]; then
    echo "Ejecutando script de inicialización de MariaDB..."
    mysql -u root -proot < /docker-entrypoint-initdb.d/setup.sql
    echo "Script de inicialización ejecutado."
fi

# Aplicar migraciones de Django
echo "Aplicando migraciones de Django..."
python manage.py makemigrations
python manage.py migrate
python seed_data.py

# Iniciar el servidor de Django
echo "Iniciando el servidor de Django..."
python manage.py runserver 0.0.0.0:8000 &

# Esperar a que MariaDB termine (cuando se detenga el contenedor)
wait $MARIADB_PID
