
# Ejemplo de SQL Injection
def obtener_usuario(usuario):
    import sqlite3
    conn = sqlite3.connect('mi_bd.db')
    cursor = conn.cursor()
    # Vulnerable: concatena entrada de usuario directamente en la consulta
    consulta = "SELECT * FROM usuarios WHERE nombre = '" + usuario + "';"
    cursor.execute(consulta)
    return cursor.fetchone()

# Ejemplo de XSS (requiere entorno web, aquí se simula la función vulnerable)
# Este ejemplo usa Flask, si tienes Django puedes modificarlo acorde.
from flask import Flask, request
app = Flask(__name__)

@app.route('/xss')
def xss():
    # Vulnerable: refleja directamente entrada del usuario
    return "Hola " + request.args.get("nombre", "")

# Ejemplo de uso inseguro de eval()
def ejecutar_codigo(codigo_usuario):
    # Vulnerable: evalúa directamente lo que pasa el usuario
    return eval(codigo_usuario)
