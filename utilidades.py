import os
import time

funciones = {
    1: "Separador",
    2: "Limpiar pantalla",
    3: "Input y salida",
    4: "Cuenta regresiva",
    5: "Cuenta regresiva dinámica",
    6: "Tamaño de un texto" 
}


###################################
# Funcion para imprimir separador 

def separador():
    print("/" , "#" * 40 , "/")

####################################
# Funcion para limpiar la pantalla 


def clear():
    os.system("clear")

##################################################################################

# Funcion para esperar input para salir.
def input_salir():
    input("Presione una tecla para salir.")

###########################################################
# Función para contar hacia atrás (por defecto 3 segundos).


def cuenta_regresiva(segundos = 3):
    for segundo in range(segundos, 0, -1): # Cuenta hacia atrás # start=3, stop=0, step=-1
        print(f"{segundo}" , end="" , flush=True) # flush=True fuerza al contenido a escribirse inmediatamente en la pantalla (en tiempo real)
        time.sleep(0.5)
        if segundo > 1: # Si no es el último número, lo acompaña una coma
            print(", " , end="" , flush=True)
            time.sleep(0.5)
    time.sleep(0.5) # Medio-segundo final que se come el if anterior.

###############################################################################
# Función para contar hacia atrás (por defecto 3 segundos). (Versión dinámica)

def cuenta_regresiva_dinamica(segundos = 3):

    for segundo in range(segundos, 0, -1): # Cuenta hacia atrás
        print(f"{segundo}"         , end="\r" , flush=True) # 9 espacios luego del segundo por si alguien quiere contar ~32 años...

        # flush=True fuerza al contenido a escribirse inmediatamente en la pantalla (en tiempo real) 
        # "\r" es un carácter de retorno de carreo. Mueve el cursor al inicio de la misma línea sin hacer un salto de línea. Si imprimís algo después, sobreescribe lo que ya estaba ahí.

        time.sleep(1) # Espera un segundo.

################################################################################

# Funcion para conocer la longitud de una cadena. 
def longitud():
    contador = 0
    tiempo = 0.1
    texto = input(" Ingrese el string. \n>> ")
    print("Cantidad de caracteres: ")
    for caracter in texto:
        if contador % 10 == 0:
            tiempo = max(tiempo/2, 0.001) # max (a, b) devuelve el mayor de los dos valores, nunca va a ser mas rapido que el promedio entre los dos porque a si a >= b y b si b >a
        contador += 1
        print(f"{contador}", end="\r" , flush=True)
        time.sleep(tiempo)

    return contador
##################################################################################
# Menú principal:
def menu_opciones():

    for clave in sorted(funciones):
        print(f"# {clave}: {funciones[clave]}")

    respuesta = (input("Seleccione una opción: ")).strip()

    if respuesta == "1": 
        separador()
        input_salir()
    elif respuesta == "2": 
        clear()
        input_salir()
    elif respuesta == "3": 
        input_salir()    
    elif respuesta == "4": 
        input_salir()
    elif respuesta == "5": 
        cuenta_regresiva_dinamica()
        input_salir()
    elif respuesta == "6":
        longitud()
        print()
        input_salir()
    else: 
        print("Elija una opción válida")
        

if __name__ == "__main__": # Si se está ejecutando directamente el módulo, lo siguiente se ejecuta:
    while True:        
        menu_opciones()
