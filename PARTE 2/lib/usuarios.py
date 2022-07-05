from . import archivo
from tkinter import messagebox
import sys


def nombre_valido(nombre):
    registro = archivo.procesar(sys.path[0] + "/db/usuarios.csv")
    valido = True

    if nombre not in registro.keys():
        if len(nombre) >= 4 and len(nombre) <= 15:
           indice = 0
           while valido and indice < len(nombre):
                caracter = nombre[indice]
                if not caracter.isalnum() and not caracter == "_":
                    valido = False
                indice +=1
        else:
            valido = False
    else:
        valido = False
	
    return valido

def clave_valida(clave):
    acentos = ["á", "Á", "é", "É", "í", "Í", "ó", "Ó", "ú", "Ú"]
    valido = True
    if len(clave) >= 8 and len(clave) <= 12:
        indice = 0
        mayusculas = 0
        minusculas = 0
        numeros = 0
        guiones = 0
        
        while valido and indice < len(clave):
            caracter = clave[indice]

            if caracter.isupper():
                mayusculas += 1
            elif caracter.islower():
                minusculas += 1
            elif caracter.isnumeric():
                numeros += 1
            elif caracter == "_" or caracter == "-":
                guiones += 1
            if caracter in acentos:
                valido = False
            indice += 1

        if not mayusculas > 0 and not minusculas > 0 and not numeros > 0 and not guiones > 0:
            valido = False

    else:
        valido = False
    
    return valido
    
def claves_iguales(clave_1, clave_2):
	valido = False
	
	if clave_1 == clave_2:
		valido = True
		clave = clave_2
		
	return {"es_valido":valido, "clave":clave}

def registrar_usuario(nombre, clave):
    archivo.escribir(sys.path[0] + "/db/usuarios.csv", ",".join([nombre, clave]))

def iniciar_sesion(usuario, clave):
    sesion_iniciada = False
    registro = archivo.procesar(sys.path[0] + "/db/usuarios.csv")
    if usuario in registro and clave == registro[usuario]:
        sesion_iniciada = True

    return sesion_iniciada