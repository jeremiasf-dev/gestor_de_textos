from utilidades import clear, separador, cuenta_regresiva 

# Creación de tablas (por única vez como se lo asignó luego de importar el módulo)

def main():

# Creación de tabla subcategorias
    ejecutar_sql("""
    CREATE TABLE IF NOT EXISTS subcategorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL DEFAULT "General"
            CHECK (length(nombre) <= 20)
            )
    """)

# Creación de tabla categorías

    ejecutar_sql("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL DEFAULT "General"
            CHECK (length(nombre) <= 20),
        subcategoria_id INTEGER NOT NULL,
        FOREIGN KEY (subcategoria_id) REFERENCES subcategorias(id)     
        )
    """)

# Creación de tabla textos y posterior relación con categorías.

    ejecutar_sql("""
        CREATE TABLE IF NOT EXISTS textos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL
            CHECK (length(titulo) <= 50),
        contenido TEXT NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """)

# Creación de valores por defecto.
## Subcategoría "General"
    ejecutar_sql("""
    INSERT INTO subcategorias (nombre)
    SELECT 'General'
    WHERE NOT EXISTS (
        SELECT 1 FROM subcategorias WHERE nombre = 'General')
    """
    )
## Categoría "General"
    ejecutar_sql("""
    INSERT INTO categorias (nombre, subcategoria_id)
    SELECT 'General', id
    FROM subcategorias
    WHERE NOT EXISTS (
        SELECT 1 FROM categorias WHERE nombre = 'General')
    """)


####################################
##### Funcion para obtener ids #####
####################################

# Subcategoría "General"
def obtener_id_subcategoria_general():

    tuplas = leer_sql(
        "SELECT id FROM subcategorias WHERE nombre = 'General'"
    )

    return tuplas[0][0] # Devuelve la primer posición de cada atributo de la entidad

# Categoría "General"
def obtener_id_categoria_general():

    tuplas = leer_sql(
        "SELECT id FROM categorias WHERE nombre = 'General'"
    )

    return tuplas[0][0] # Devuelve la primer posición de cada atributo de la entidad


######################################
# Funcion para agregar subcategorías #
######################################

def agregar_subcategoria():
    while True:

        clear()
        separador()
        print("# Subcategoría:")
        print("# Presiona enter para no elegir una categoría.")
        separador()
        
        subcategoria = input(">> ").strip() # .strip() sanitiza los espacios al principio y al final del input.

        # Si el usuario no ingresa nada, devuelve "General".
        if not subcategoria: # Porque un string vacío es "sinónimo" de False.
            return "General"
        
        # Si la subcategoría no existe, pregunta si desea añadirla.
        else:     
            respuesta = input(f"'{subcategoria}' no existe, desea agregarla? (y/n)").strip().upper()
            
            if respuesta == "Y":
                return subcategoria
            if respuesta == "N":
                continue # Vuelve a pedir una subcategoría.
            else: # Imprime un mensaje, hace una espera visual de tres segundos y vuelve pedir una subcategoría.
                print("Por favor. Ingrese 'y' para sí o 'n' para no. (Sin las comillas)")
                cuenta_regresiva() # Pausa 3 segundos antes de volver a borrar la pantalla.
                continue
            
        
        
###################################
# Funcion para agregar categorías #
###################################

def agregar_subcategoria():

    while True:

        clear()
        
        separador()
        
        print("# Categoría:")
        print("# Presiona enter para no elegir una categoría.")
        
        separador()
        
        categoria = input(">> ").strip() # .strip() sanitiza los espacios al principio y al final del input.

        if categoria == "":
            # Solo se retorna el ID de la subcategoría "General"
            return obtener_id_categoria_general()

        else:

            # Bucle de Confirmación.#

            while True:
                clear()
                
                separador()

                print(f"# La categoría '{categoria}' no existe. ¿Deseas agregarla?")
                print("y/n")

                separador()

                respuesta = input(">> ").strip().upper() # Quita los espacios y convierte el texto a mayúsculas.
                
                if respuesta == "Y":
                    # Se inserta una nueva subcategoría y se cierra la selección de subcategoría. Retorna su id .
                    id_nueva_categoria = ejecutar_sql(
                        "INSERT INTO categorias (nombre) VALUES (?)",
                        (categoria,)
                    )
                    return id_nueva_subcategoria
                elif respuesta == "N":
                    break
                else:
                    print("Por favor. Ingrese 'y' para sí o 'n' para no. (Sin las comillas)")
                    cuenta_regresiva() # Pausa 3 segundos antes de reiniciar el bucle.

##################################################
#### Funcion para agregar el título del texto ####
##################################################

def agregar_titulo():

    clear()
    
    separador()
    
    print("# Título:")
    print("# Presiona enter para no elegir un título.")
    
    separador()
    
    # Input del usuario, si aprieta enter, la nota pasa a llamarse "Sin titulo".      
    # Esta forma es muy interesante, porque es como python maneja algunas cosas.
    # Los "or" devuelven primero el valor verdadero.
    # En python, hay "sinonimos" de "False": "" , 0 , NONE , () , [] , []
    # Por ende, si el usuario ingresa algo, ese algo se guarda en la variable,
    # y, si no ingresa nada, pasa a valer el próximo valor verdadero: "Sin título"
    titulo = input(">> ").strip() or "Sin titulo"
    ejecutar_sql("INSERT INTO textos (titulo) VALUES (?)", (titulo,))

################################################
# Funcion para agregar el contenido del texto. #
################################################

def agregar_contenido_del_texto():

    clear()

    print("# Nota:")

    print()

    texto = input("").strip() or "Sin contenido"
    ejecutar_sql("INSERT INTO textos (texto) VALUES (?)", (texto,))

    separador()

####################################
# Función para crear el texto/nota #
####################################
def crear_nota():
    agregar_contenido_del_texto()
    agregar_subcategoria()




# Bucle del programa

main()
crear_nota()

# Próximanente