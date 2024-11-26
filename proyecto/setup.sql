-- Establecer contraseña para el usuario root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';

-- Eliminar usuarios anónimos
DELETE FROM mysql.user WHERE User='';

-- Eliminar la base de datos de prueba
DROP DATABASE IF EXISTS test;

-- Crear la base de datos para la aplicación Django
CREATE DATABASE IF NOT EXISTS dbpgpipaas CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- Crear el usuario 'pgpipaas_user' con contraseña
CREATE USER IF NOT EXISTS 'pgpipaas_user'@'localhost' IDENTIFIED BY 'pgpipaas_password';

GRANT ALL PRIVILEGES ON dbpgpipaas.* TO 'pgpipaas_user'@'host.docker.internal' IDENTIFIED BY 'pgpipaas_password';
FLUSH PRIVILEGES;

-- Otorgar todos los privilegios sobre la base de datos al usuario
GRANT ALL PRIVILEGES ON dbpgpipaas.* TO 'pgpipaas_user'@'localhost' IDENTIFIED BY 'pgpipaas_password';

-- Aplicar los cambios de privilegios
FLUSH PRIVILEGES;

GRANT SELECT ON mysql.* TO 'pgpipaas_user'@'localhost';
FLUSH PRIVILEGES;

-- Configurar el modo SQL
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES';