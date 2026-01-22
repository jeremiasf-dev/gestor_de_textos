from db import ejecutar_sql, leer_sql
from utilidades import clear, separador, cuenta_regresiva, cuenta_regresiva_dinamica

# Creación de tablas (por única vez como se lo asignó luego de importar el módulo)

def main():

# Creación de tabla subcategorias
    ejecutar_sql("""
    CREATE TABLE IF NOT EXISTS subcategorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE CHECK (length(nombre) <= 20)
        )
    """)

# Creación de tabla categorías

    ejecutar_sql("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE CHECK (length(nombre) <= 20),
        subcategoria_id INTEGER NOT NULL,
        FOREIGN KEY (subcategoria_id) REFERENCES subcategorias(id)
        )
    """)

# Creación de tabla textos y posterior relación con categorías.

    ejecutar_sql("""
        CREATE TABLE IF NOT EXISTS textos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL CHECK (length(titulo) <= 50),
        contenido TEXT NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """)

# Creación de valores por defecto.
## Subcategoría "General"
    ejecutar_sql("""
        INSERT OR IGNORE INTO subcategorias (nombre) VALUES ('GENERAL');
    """ 
    )
## Categoría "General"

    ejecutar_sql("""
        INSERT OR IGNORE INTO categorias (nombre, subcategoria_id) VALUES ('GENERAL', ?);
    """, (obtener_id_subcategoria_general(), ))

# Funciones varias

####################################
##### Funcion para obtener ids #####
####################################

# Subcategoría "General"
def obtener_id_subcategoria_general():

    tuplas = leer_sql(
        "SELECT id FROM subcategorias WHERE nombre = 'GENERAL'"
    )

    return tuplas[0][0] # Devuelve una lista de tuplas. El primer índice accede a la tupla, el segundo, al atributo.

# Categoría "General"
def obtener_id_categoria_general():

    tuplas = leer_sql(
        "SELECT id FROM categorias WHERE nombre = 'GENERAL'"
    )

    return tuplas[0][0]

# Funciones primarias

###########################################
# Funcion general para agregar categorías #
###########################################

def agregar_categoria(tipo):

    nombres = {0: "Subcategoría", 1: "Categoría"}
    tipo_nombre = nombres[tipo]

    while True:

        clear()
        print(f" {tipo_nombre}: ")
        print("# Presiona enter para categoría por defecto.")

        # Ingresa el nombre de la categoría.
        item = input(">> ").strip().upper() # .strip() sanitiza los espacios al principio y al final del input. Se recibe el string en mayúsculas para normalizar nombres de categorías.

        # Si el usuario no ingresa nada, devuelve "General".
        if not item: # Porque un string vacío es "sinónimo" de False.
            return "GENERAL"

        # Si no existe, pregunta si desea añadirla.
        else:
            respuesta = input(f"'{tipo_nombre}' no existe, desea agregarla? (y/n) \n>> ").strip().upper()

            if respuesta == "Y":
                return item
            if respuesta == "N":
                continue # Vuelve a pedir una categoria.
            else: # Imprime un mensaje, hace una espera visual de tres segundos y vuelve pedir una categoria.
                clear()
                print("Error. Por favor. Ingrese 'y' para sí o 'n' para no. (Sin las comillas)")
                cuenta_regresiva() # Pausa 3 segundos antes de volver a borrar la pantalla.
                continue

##################################################
#### Funcion para agregar el título del texto ####
##################################################

def agregar_titulo():

    clear()
    print("# Título:")

    # Input del usuario, si aprieta enter, la nota pasa a llamarse "Sin titulo". 
    # Esta forma es muy interesante, porque es como python maneja algunas cosas.
    # Los "or" devuelven primero el valor verdadero.
    # En python, hay "sinonimos" de "False": "" , 0 , NONE , () , [] , []
    # Por ende, si el usuario ingresa algo, ese algo se guarda en la variable,
    # y, si no ingresa nada, pasa a valer el próximo valor verdadero: "Sin título"

    titulo = input(">> ").strip() or "Sin título"
    return titulo

################################################
# Funcion para agregar el contenido del texto. #
################################################

def agregar_contenido_del_texto():

    clear()
    print("# Nota:\n")

    contenido = input("").strip() or "Sin contenido"
    return contenido

########################################
# Funcion para mostrar todas las notas #
########################################

def mostrar_notas():
    # Trae todas las notas junto con la categoría asociada
    notas = leer_sql("""
        -- Proyecto todos los atributos salvo el id...
        SELECT textos.titulo, textos.contenido, categorias.nombre AS categoria,
        subcategorias.nombre AS subcategoria
        
        -- ...de la tabla textos.        
        FROM textos
        
        -- Combino las categorias y subcategorias a la proyección (INNER JOIN solo devuelve tuplas que tienen coincidencias en todas las tablas unidas. )
          
        JOIN categorias ON textos.categoria_id = categorias.id
        JOIN subcategorias ON categorias.subcategoria_id = subcategorias.id
        
        -- Ordeno de > id

        ORDER BY textos.id
    """)

    if not notas:
        print("Aún no existen notas.")
        cuenta_regresiva()
        return

    for nota in notas:
        titulo, contenido, categoria, subcategoria = nota
        if nota:
            separador()
            print(f"Categoría: {categoria}.")
            print(f"Subcategoría: {subcategoria}.")
            separador()
            print(f"\n{titulo}\n")
            print(f"{contenido}")
            separador()


############################################################################
# Funcion para buscar notas por coincidencia parcial en titulo y contenido #
############################################################################

def buscar_notas(palabra):

    # La función se está ejecutando
    en_ejecucion = True

    # Agrega % al inicio y al final para coincidencia parcial
    filtro = f"%{palabra}%"

    notas = leer_sql("""
        SELECT textos.titulo, textos.contenido, categorias.nombre AS categoria,
        subcategorias.nombre AS subcategoria

        FROM textos
        
        JOIN categorias ON textos.categoria_id = categorias.id
        JOIN subcategorias ON categorias.subcategoria_id = subcategorias.id

        -- Busqueda por coincidencia parcial

        WHERE textos.titulo LIKE ? COLLATE NOCASE OR textos.contenido LIKE ?
        ORDER BY textos.id
    """, (filtro, filtro))

    if not notas:
        print(f"No se encontraron notas con '{palabra}'. intente con otra palabra.")
        cuenta_regresiva()
        return

    for nota in notas:
        titulo, contenido, categoria, subcategoria = nota
        separador()
        print(f"Título: {titulo}")
        print(f"Categoría: {categoria}")
        print(f"Subcategoría: {subcategoria}")
        print(f"Contenido: {contenido}")
        
        separador()
        print()

####################################
# Función para crear el texto/nota #
####################################
def crear_nota(nota = ""):
    # Comienza pidiendo el contenido del texto, luego el título, la subcategoría y la categoría.
    contenido = agregar_contenido_del_texto()
    titulo = agregar_titulo()

    nombre_subcategoria = agregar_categoria(0) # 0 = key de subcategoria
    nombre_categoria = agregar_categoria(1)    # 1 = key de categoria

    # Inserción de subcategoría

    if nombre_subcategoria == "GENERAL" :
        subcategoria_id = obtener_id_subcategoria_general()
    else:
        # Inserto la nueva categoría si no existe
        ejecutar_sql(
            "INSERT OR IGNORE INTO subcategorias (nombre) VALUES (?)",
            (nombre_subcategoria, )
        )

        subcategoria_id = leer_sql("SELECT id FROM subcategorias WHERE nombre = ?", (nombre_subcategoria,))[0][0]

   # Inserción de categoría

    if nombre_categoria == "GENERAL" :
        categoria_id = obtener_id_categoria_general()
    else:
        # Inserto la nueva categoría si no existe y capturo su id
        ejecutar_sql(
            "INSERT OR IGNORE INTO categorias (nombre, subcategoria_id) VALUES (?, ?)",
            (nombre_categoria, subcategoria_id)
        )
        categoria_id = leer_sql("SELECT id FROM categorias WHERE nombre = ?", (nombre_categoria,))[0][0]

    # Inserto la nota en la tabla textos
    ejecutar_sql(
        "INSERT INTO textos (titulo, contenido, categoria_id) VALUES (?, ?, ?)",
        (titulo, contenido, categoria_id)
    )
    clear()
    print("Nota creada con éxito.")
    cuenta_regresiva(2)


# Modo debug

def debug():
    corriendo = True
    while corriendo:
        print("Datos en textos:")
        print(leer_sql("SELECT * FROM textos"))
        print()
        print("Datos en categorias:")
        print(leer_sql("SELECT * FROM categorias"))
        print("Datos en subcategorías:")
        print(leer_sql("SELECT * FROM subcategorias"))
        respuesta = input("1 para continuar, 0 para volver a mostrar.").strip()
        if respuesta == "0":
            continue
        else:
            return False
            
# Menu principal

def menuprincipal():
    while True:
        clear()
        print("1) Crear nota.")
        print("2) Búsqueda.")
        print("3) Mostrar notas.")
        print("4) Modo debug")
        print("0) Salir del programa.")

        opcion = int(input(">> ").strip())

        if opcion == 1:
            crear_nota()
        elif opcion == 2:
            buscar_notas(input("\n Ingrese palabra a buscar. \n>> ").strip())
        elif opcion == 3:
            mostrar_notas()
        elif opcion == 4:
            debug()
        elif opcion == 0:
            return False
        else:
            print("Error. Ingrese una opción válida.")
            cuenta_regresiva()

#####################################################################################################################################
#####################################################################################################################################

# Bucle del programa

try:
    ## Inicialización de la base de datos y carga de la categoría y subcategoría "General".
    main()
    
    ## Aplicación ##
    menuprincipal()
    ## Fin aplicación ##

except(ValueError):
    clear()
    print("Error, ingrese una opción válida.")
    cuenta_regresiva_dinamica(2)
except Exception as e:
    clear()
    print(f"Error: {e}")
    cuenta_regresiva(5)

# Próximanente
