# Creación de tablas (por única vez como se lo asignó luego de importar el módulo)

def main():

# Creación de tabla categorías
    ejecutar_sql("""
    CREATE TABLE categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL DEFAULT "General"
            CHECK (length(titulo) <= 15)
    )
    """)

# Creación de tabla textos y posterior relación con categorías.

    ejecutar_sql("""
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

#################################
# Funcion para crear categorías #
#################################



#################################
#### Funciones para el texto ####
#################################






conn.commit() # Confirmo los cambios
conn.close()  # Cierro la conexión con la base de datos.
