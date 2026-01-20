import time
from utilidades import clear, separador, cuenta_regresiva 

# Creación de tablas (por única vez como se lo asignó luego de importar el módulo)

def main():

# Creación de tabla subcategorias
    ejecutar_sql("""
    CREATE TABLE IF NOT EXISTS subcategorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL DEFAULT "General"
            CHECK (length(titulo) <= 20)
            )
    """)

# Creación de tabla categorías

    ejecutar_sql("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL DEFAULT "General"
            CHECK (length(titulo) <= 20),
        subcategoria_id INTEGER NOT NULL,
        FOREIGN KEY (subcategoria_id) REFERENCES subcategorias(id)     
        )
    """)

# Creación de tabla textos y posterior relación con categorías.

    ejecutar_sql("""
        CREATE TABLE IF NOT EXISTS textos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL DEFAULT "Nota"
            CHECK (length(titulo) <= 50),
        contenido TEXT NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """)

# Creación de valores por defecto.
## Subcategoría
    ejecutar_sql("""
    INSERT INTO subcategorias (titulo)
    SELECT 'General'
    WHERE NOT EXISTS (
        SELECT 1 FROM subcategorias WHERE titulo = 'General')
    """
    )
## Categoría
    ejecutar_sql("""
    INSERT INTO categorias (titulo, subcategoria_id)
    SELECT 'General', id
    FROM subcategorias
    WHERE NOT EXISTS (
        SELECT 1 FROM categorias WHERE titulo = 'General')
    """)


####################################
##### Funcion para obtener ids #####
####################################

# Subcategoría "General"
def obtener_id_subcategoria_general():

    tuplas = leer_sql(
        "SELECT id FROM subcategorias WHERE titulo = 'General'"
    )

    return tuplas[0][0] # Devuelve la primer posición de cada atributo de la entidad

####################################
# Funcion para crear subcategorías #
####################################

def crear_subcategoria():
    while True:
        clear()
        
        separador()
        
        print("# Subcategoría:")
        print("# Presiona enter para no elegir una categoría.")
        
        separador()
        
        subcategoria = input(">> ").strip() # .strip() sanitiza los espacios al principio y al final del input.

        if subcategoria == "":
            # Solo se retorna el ID de la subcategoría "General"
            return obtener_id_subcategoria_general()

        else:

            # Bucle de Confirmación.#

            while True:
                clear()
                
                separador()

                print(f"# La subcategoría '{subcategoria}' no existe. ¿Deseas agregarla?")
                print("y/n")

                separador()

                respuesta = input(">> ").strip().upper() # Quita los espacios y convierte el texto a mayúsculas.
                
                if respuesta == "Y":
                    # Se inserta una nueva subcategoría y se cierra la selección de subcategoría. Retorna su id .
                    id_nueva_subcategoria = ejecutar_sql(
                        "INSERT INTO subcategorias (titulo) VALUES (?)",
                        (subcategoria,)
                    )
                    return id_nueva_subcategoria
                elif respuesta == "N":
                    break
                else:
                    print("Por favor. Ingrese 'y' para sí o 'n' para no. (Sin las comillas)")
                    time.sleep(3) # Pausa 2 segundos antes de volver a borrar la pantalla.

#################################
# Funcion para crear categorías #
#################################

def crear_categoria():
    while True:

        clear()
        separador()                

        # Se determina la subcategoría
        subcategoria_id = crear_subcategoria()

        print(" Categoría:")
        categoria = input(">> ")        

        # Si el usuario no ingresó nombre, se usa "General"
        if categoria == "":
            categoria = "General"
        # Se inserta la categoría con su correspondiente subcategoría
        ejecutar_sql(
            "INSERT INTO categorias (titulo, subcategoria_id) VALUES (?, ?)",
            (categoria, subcategoria_id)
        )
        break


#################################
#### Funciones para el texto ####
#################################

# Se inicializan las funciones
main()

# Bucle del programa

# Próximanente