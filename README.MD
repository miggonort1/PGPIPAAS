para instalar el entorno virtual: 
- python3 -m venv env
- env\Scripts\activate

- pip install django

PASOS PARA CONFIGURAR LA BASE DE DATOS
 
-Escribir en cmd "mariadb --version" para comprobar si ya teneis mariadb instalado y no teneis que seguir con los demas pasos, si es asi pasar a seeds
- Descargar mariadb desde la pagina web VERSION 11.5
- Abrir el instalador y seguir los pasos poniendo
    - Contraseña "root"
- Abrir las variables de entorno y poner en dentro del path variables del sistema "C:\Program Files\MariaDB 11.5\bin"
- Escribir en el cmd "mariabd --version"
- Si no os da una version reiniciar el ordenador

Ahora dentro del entorno virtual
- mariadb -u root -p
-   CREATE DATABASE dbpgpipaas CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

    CREATE USER 'pgpipaas_user'@'localhost' IDENTIFIED BY 'pgpipaas_password';
    GRANT ALL PRIVILEGES ON dbpgpipaas.* TO 'pgpipaas_user'@'localhost';
    FLUSH PRIVILEGES;


CERRAMOS EL MARIADB

MIGRATION
- python manage.py makemigrations;
- python manage.py migrate;




SEEDS
- Escribir el codigo para introducir en los seeds
- Para hacer el seed "python seed_data.py"



PARA ARRANCAR EL SERVER LOCAL
- Te metes en el entorno virtual
 source env/Scripts/activate

 - Desde la carpeta proyecto 
 python manage.py runserver



CORREO:
- Email: pgpipaas@gmail.com
- Contraseña: pgpipaas1234
- Contraseña(aplicacion): jqbb eueg fwfq gpaw


 USUARIO            CONTRASEÑA
 pgpipaas1          1234
 pgpipaas2          1234
 admin1             1234