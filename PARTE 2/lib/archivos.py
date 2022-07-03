import string
from . import cadenas
import sys

def leer_linea(archivo, separador, default):
  linea = archivo.readline()
  return linea.rstrip("\n").split(separador) if linea else default



def procesar_config(config):
    linea_config = leer_linea(config, ",", ",")
    configuracion = {}
    while linea_config != ",":
        linea_temp = linea_config
        while linea_config != "," and linea_temp == linea_config:
            configuracion[linea_temp[0]] = linea_temp[1]
            linea_config = leer_linea(config, ",", ",")
    return configuracion

# def procesar_archivo(archivo, configuracion, palabras_secretas):
#     repeticiones = {}
#     linea = leer_linea(archivo, " ", "")
#     while linea:
#         linea_temp = linea
        
#         while linea and linea_temp == linea:
#             i = 0
#             cont_cadena = 1
#             while linea and linea_temp == linea and i < len(linea_temp):
#                 cadena_ = linea_temp[i].strip(string.punctuation)
#                 cadena = cadenas.formatear_palabra(cadena_)
                
#                 if cadena in palabras_secretas:
#                     cont_cadena += 1
#                     repeticiones[cadena] = cont_cadena
#                 else: 
#                     if cadena.isalpha() and len(cadena) == int(configuracion["LONGITUD_PALABRA_SECRETA"]):
#                         palabras_secretas.append(cadena)
#                 i+=1
#             linea = leer_linea(archivo, " ", "")
#     repeticiones_ord = sorted(repeticiones.items())
#     return repeticiones_ord

# def merge(archivo_1, archivo_2, archivo_3, palabras):
#     linea_1 = leer_linea(archivo_1, " ", "")
#     linea_2 = leer_linea(archivo_2, " ", "")
#     linea_3 = leer_linea(archivo_3, " ", "")
#     configuracion = procesar_config(config)
#     lista = []
#     repeticiones_1 = procesar_archivo(archivo_1, configuracion, lista)
#     repeticiones_2 = procesar_archivo(archivo_2, configuracion, lista)
#     repeticiones_3 = procesar_archivo(archivo_3, configuracion, lista)
    
    
#     lista_ord = sorted(lista)
#     dicc_ord = {"palabras_secretas":lista_ord}
#     return dicc_ord

def leer_archivo(archivo):
    linea = archivo.readline()
    if linea:
        linea = linea.rstrip("\n")
    else:
        linea = ","

    return linea.split(",")


def procesar_archivo(ruta_archivo):
    with open(ruta_archivo, "r") as archivo:
        clave, valor = leer_archivo(archivo)
        registro = { clave: valor }
        while clave:
            registro[clave] = valor
            clave, valor = leer_archivo(archivo)

    return registro

def escribir_archivo(ruta_archivo, cadena):
  archivo = open(ruta_archivo, "a")
  archivo.write(cadena)

def guardar_nuevos_datos(nuevo_usuario, nueva_clave):
    with open (sys.path[0] + "/db/usuarios.csv", "a") as archivo:
        linea = f"{nuevo_usuario},{nueva_clave}\n"
        archivo.write(linea)
    
    return
