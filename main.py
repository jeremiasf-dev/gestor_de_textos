from db import ejecutar_sql, leer_sql
from utilidades import clear, separador, cuenta_regresiva, cuenta_regresiva_dinamica

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

        
###########################################
# Funcion general para agregar categorías #
###########################################

def agregar_categoria(tipo):

    nombres = {0: "Subcategoría", 1: "Categoría"}
    tipo_nombre = nombres[tipo]

    while True:

        clear()
        
        separador()
        print(f" {tipo_nombre}: ")
        print("# Presiona enter para no elegir una.")
        separador()
        
        # Devuelve un item del diccionario.
        item = input(">> ").strip() # .strip() sanitiza los espacios al principio y al final del input.

        # Si el usuario no ingresa nada, devuelve "General".
        if not item: # Porque un string vacío es "sinónimo" de False.
            return "General"
        
        # Si no existe, pregunta si desea añadirla.
        else:     
            respuesta = input(f"'{tipo_nombre}' no existe, desea agregarla? (y/n)").strip().upper()
            
            if respuesta == "Y":
                return item
            if respuesta == "N":
                continue # Vuelve a pedir una categoria.
            else: # Imprime un mensaje, hace una espera visual de tres segundos y vuelve pedir una categoria.
                print("Por favor. Ingrese 'y' para sí o 'n' para no. (Sin las comillas)")
                cuenta_regresiva() # Pausa 3 segundos antes de volver a borrar la pantalla.
                continue

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
    titulo = input(">> ").strip() or "Sin título"
    return titulo

################################################
# Funcion para agregar el contenido del texto. #
################################################

def agregar_contenido_del_texto():

    clear()
    print("# Nota:")
    print()

    contenido = input("").strip() or "Sin contenido"
    return contenido

####################################
# Función para crear el texto/nota #
####################################
def crear_nota():
    
    # Comienza pidiendo el contenido del texto, luego el título, la subcategoría y la categoría.
    contenido = agregar_contenido_del_texto()
    titulo = agregar_titulo()    

    nombre_subcategoria = agregar_categoria(0)
    nombre_categoria = agregar_categoria(1)
    
    if nombre_subcategoria == "General":
        subcategoria_id = obtener_id_subcategoria_general()
    else:
        # Capturo su el id de la subcategoría a punto de ingresar
        ejecutar_sql(
            "INSERT INTO subcategorias (nombre) VALUES (?)",
            (nombre_subcategoria, )
        )
        # Hago insert a través de su id.
        
        subcategoria_id = leer_sql("SELECT id FROM subcategorias WHERE nombre = ?", (nombre_subcategoria,))[0][0]

    if nombre_categoria == "General" :
        categoria_id = obtener_id_categoria_general()
    else:
        # Inserto la nueva categoría si no existe y capturo su id
        ejecutar_sql(
            "INSERT INTO categorias (nombre, subcategoria_id) VALUES (?, ?)",
            (nombre_categoria, subcategoria_id)
        )
        categoria_id = leer_sql("SELECT id FROM categorias WHERE nombre = ?", (nombre_categoria))[0][0]

    # Inserto la nota en la tabla textos
    ejecutar_sql(
        "INSERT INTO textos (titulo, contenido, categoria_id) VALUES (?, ?, ?)",
        (titulo, contenido, categoria_id)
    )
    clear()
    separador()
    print("Nota creada con éxito.")


############################################################################
# Funcion para buscar notas por coincidencia parcial en titulo y contenido #
############################################################################

def buscar_notas(palabra):
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


# Bucle del programa
## Inicialización de la base de datos y carga de la categoría y subcategoría "General".
main()
debug = True
# Menú interactivo
try:
    while True:
    ## Sección debug
        print("Datos en textos:")
        print(leer_sql("SELECT * FROM textos"))
        print()
        print("Datos en categorias:")
        print(leer_sql("SELECT * FROM categorias"))

        while debug:
            respuesta = input("Presione enter para continuar. \n>>")

            if respuesta == "":
                debug = False
                continue
            else:
                continue
    ## Fin sección debug

        print("Presione enter para continuar")
        clear()
        print("1) Crear nota.")
        print("2) Búsqueda.")
        print("3) Mostrar notas(DEBUG).")
        print("0) Salir del programa.")

        opcion = int(input(">> ").strip())

        if opcion == 1:
            crear_nota()
        elif opcion == 2:
            buscar_notas(input("\n Ingrese palabra a buscar. \n>> ").strip())
        elif opcion == 3:
            mostrar_notas()
        elif opcion == 0:
            break
        else:
            print("Error. Ingrese un número (0 incluído)")
            cuenta_regresiva()
except(ValueError):
    print("Error, ingrese un numero entero.")
    cuenta_regresiva_dinamica()

# Próximanente