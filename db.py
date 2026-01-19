# Base de datos
# Importación de sqlite y creación de la base de datos

import sqlite3

# Función para conectarse a la base de datos
def conectar():
    """
    Crea una conexión a la base de datos SQLite y activa claves foráneas.
    Devuelve un objeto connection.
    """
    conn = sqlite3.connect("app.db")
    conn.execute("PRAGMA foreign_keys = ON")  # Garantiza integridad referencial
    return conn

# Creo un cursor para ejecutar SQL
def ejecutar_sql(sql, parametros=None):
    conn = conectar()
    cursor = conn.cursor()

    if parametros:
        cursor.execute(sql, parametros)
    else:
        cursor.execute(sql)
    conn.commit() # Hace commit si subo INSERT/UPDATE/DELETE/CREATE
    conn.close()  # Cierra la conexión con la base de datos


# Función para ejecutar SELECT y devolver resultados
def leer_sql(sql, parametros=None):
    """
    Ejecuta una consulta SELECT y devuelve todos los resultados.
    - sql: cadena con la sentencia SQL
    - parametros: tupla con valores a filtrar en la consulta (opcional)
    Retorna una lista de tuplas con los resultados.
    """
    conn = conectar()
    cursor = conn.cursor()
    if parametros:
        cursor.execute(sql, parametros)
    else:
        cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.close()
    return resultados


