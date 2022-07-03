import string
from fiuble import *

def leer_info_txt(archivo, default):
    linea = archivo.readline()
    return linea.rstrip("\n").split(' ') if linea else default

def leer_info_csv(archivo, default):
    linea = archivo.readline()
    return linea.rstrip("\n").split(',') if linea else default

def procesar_config(config):
    linea_config = leer_info_csv(config, ",")
    configuracion = {}
    while linea_config != ",":
        linea_temp = linea_config
        while linea_config != "," and linea_temp == linea_config:
            configuracion[linea_temp[0]] = linea_temp[1]
            linea_config = leer_info_csv(config, ",")
    return configuracion

def procesar_archivo(archivo, configuracion, palabras_secretas):
    repeticiones = {}
    linea = leer_info_txt(archivo, "")
    while linea:
        linea_temp = linea
        
        while linea and linea_temp == linea:
            i = 0
            cont_cadena = 1
            while linea and linea_temp == linea and i < len(linea_temp):
                cadena_ = linea_temp[i].strip(string.punctuation)
                cadena = formatear_palabra(cadena_)
                
                if cadena in palabras_secretas:
                    cont_cadena += 1
                    repeticiones[cadena] = cont_cadena
                else: 
                    if cadena.isalpha() and len(cadena) == int(configuracion["LONGITUD_PALABRA_SECRETA"]):
                        palabras_secretas.append(cadena)
                i+=1
            linea = leer_info_txt(archivo, "")
    repeticiones_ord = sorted(repeticiones.items())
    return repeticiones_ord

def merge(archivo_1, archivo_2, archivo_3, palabras):
    linea_1 = leer_info_txt(archivo_1, "")
    linea_2 = leer_info_txt(archivo_2, "")
    linea_3 = leer_info_txt(archivo_3, "")
    configuracion = procesar_config(config)
    lista = []
    repeticiones_1 = procesar_archivo(archivo_1, configuracion, lista)
    repeticiones_2 = procesar_archivo(archivo_2, configuracion, lista)
    repeticiones_3 = procesar_archivo(archivo_3, configuracion, lista)
    
    
    lista_ord = sorted(lista)
    dicc_ord = {"palabras_secretas":lista_ord}
    return dicc_ord


archivo_1 = open ("D:\FIUBA\Algoritmos y Programacion I\TP-FIUBLE\FIUBLE\PARTE 2\Cuentos.txt", "r")
archivo_2 = open ("D:\FIUBA\Algoritmos y Programacion I\TP-FIUBLE\FIUBLE\PARTE 2\La araña negra - tomo 1.txt", "r")
archivo_3 = open ("D:\FIUBA\Algoritmos y Programacion I\TP-FIUBLE\FIUBLE\PARTE 2\Las 1000 Noches y 1 Noche.txt", "r")
palabras = open ("D:\FIUBA\Algoritmos y Programacion I\TP-FIUBLE\FIUBLE\PARTE 2\palabras.csv", "w")
config = open ("D:\FIUBA\Algoritmos y Programacion I\TP-FIUBLE\FIUBLE\PARTE 2\configuracion.csv", "r")
dicc = merge(archivo_1, archivo_2, archivo_3, palabras)
print (dicc)
# print(procesar_config(config))

archivo_1.close()
archivo_2.close()
archivo_3.close()
palabras.close()
config.close()