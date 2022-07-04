import string
from . import cadenas

SEPARADOR_CSV = ","
SEPARADOR_TXT = " "

def leer_linea(archivo, separador, default = ["", ""]):
  linea = archivo.readline()
  return linea.rstrip("\n").split(separador) if linea else default

def combinar_cuentos(cuentos, longitud_palabras):
    palabras = {}
    for indice, cuento in enumerate(cuentos):
        archivo = open(cuento)

        linea = leer_linea(archivo, SEPARADOR_TXT, "")

        while linea:
            for palabra in linea:
                palabra_limpia = palabra.strip(string.punctuation)
                if palabra_limpia.isalpha() and len(palabra_limpia) == int(longitud_palabras):
                    palabra_formateada = cadenas.formatear_palabra(palabra_limpia)
                    if not palabra_formateada in palabras:
                        palabras[palabra_formateada] = [0 for x in range(len(cuentos))]
                    palabras[palabra_formateada][indice] += 1
            linea = leer_linea(archivo, SEPARADOR_TXT, "")
        archivo.close()
    
    return palabras

def procesar_archivo(ruta_archivo):
    archivo = open(ruta_archivo, "r")
    extension = archivo.name.split(".")[-1]
    separador = SEPARADOR_CSV if extension == "csv" else SEPARADOR_TXT

    registro = {}
    linea = leer_linea(archivo, separador)
    while linea[0]:
        valor = linea[1:len(linea)]
        registro[linea[0]] = valor[0] if valor else ""
        linea = leer_linea(archivo, separador)

    return registro

def escribir_archivo(ruta_archivo, cadena):
  archivo = open(ruta_archivo, "a")
  archivo.write(cadena)
  archivo.close()

def vaciar_archivo(ruta_archivo):
  archivo = open(ruta_archivo, "w")
  archivo.write("")
  archivo.close()