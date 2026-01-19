# Base de datos
# Importación de sqlite y creación de la base de datos

import sqlite3

# Intenta conectar con el archivo (.db), si no existe, lo crea.
conn = sqlite3.connect("app.db")

# El cursor (ejemplo: una persona que atiende un celular) ejecuta sentencias SQL.
# La conexión (ejemplo: el celular), la transacción y el archivo.
cursor = conn.cursor()
# Activa las claves foráneas.
cursor.execute("PRAGMA foreign_keys = ON")

# Ejecuto el cursor: Creación de tablas

cursor.execute("""
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL DEFAULT "General"
        CHECK (length(titulo) <= 15)
)
""")
cursor.execute("""
CREATE TABLE textos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL DEFAULT "Nota"
        CHECK (length(titulo) <= 50),
    contenido TEXT NOT NULL
        CHECK (length(contenido) <=50),
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)
""")

conn.commit() # Confirmo los cambios
conn.close()  # Cierro la conexión con la base de datos.



