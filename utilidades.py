import os
import time

###################################
# Funcion para imprimir separador 
###################################
def separador():
    print("/" , "#" * 18 , "/")

####################################
# Funcion para limpiar la pantalla 
####################################

def clear():
    os.system("clear")

###########################################################
# Función para contar hacia atrás (por defecto 3 segundos).
###########################################################

def cuenta_regresiva(segundos = 3):
    for segundo in range(segundos, 0, -1): # Cuenta hacia atrás # start=3, stop=0, step=-1
        print(f"{segundo}" , end="" , flush=True) # flush=True fuerza al contenido a escribirse inmediatamente en la pantalla (en tiempo real)
        time.sleep(0.5)
        if segundo > 1: # Si no es el último número, lo acompaña una coma
            print(", " , end="" , flush=True)
            time.sleep(0.5)
    time.sleep(0.5) # Medio-segundo final que se come el if anterior.

###############################################################################
# Función para contar hacia atrás (por defecto 3 segundos). (Versión dinámica)#
###############################################################################

def cuenta_regresiva_dinamica(segundos = 3):

    for segundo in range(segundos, 0, -1): # Cuenta hacia atrás
        print(f"{segundo}"         , end="\r" , flush=True) # 9 espacios luego del segundo por si alguien quiere contar ~32 años...

        # flush=True fuerza al contenido a escribirse inmediatamente en la pantalla (en tiempo real) 
        # "\r" es un carácter de retorno de carreo. Mueve el cursor al inicio de la misma línea sin hacer un salto de línea. Si imprimís algo después, sobreescribe lo que ya estaba ahí.

        time.sleep(1) # Espera un segundo.


# Debug
# if __name__ == "__main__":
    # Esto solo se ejecuta si corro el módulo directamente.
