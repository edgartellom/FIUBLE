from manejo_archivo_usuarios import *
from tkinter import messagebox


def nombre_valido(nombre):
    registro = procesar_archivo()
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
            elif caracter.isdigit():
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

def guardar_registro(nombre, clave_1, clave_2):
    registro = procesar_archivo()
    
    if nombre_valido(nombre):
        
        if clave_valida(clave_1) and clave_valida(clave_2):
            claves_coinciden = claves_iguales(clave_1, clave_2)
            if claves_coinciden["es_valido"]:
                clave = claves_coinciden["clave"]
                guardar_nuevos_datos(nombre, clave)
                messagebox.showinfo("Registro", "Usuario y Clave registrados con éxito!")

            else:
                messagebox.showerror("Registro", "Claves ingresadas no coinciden!")

        else:
            messagebox.showerror("Registro", "Clave ingresada inválida! Debe ser entre 8 y 12 caracteres y contener al menos una minúscula, una mayúscula, un número y un guión ('-' o '_')")
    
    else:
        messagebox.showerror("Registro", "Nombre ingresado inválido! Debe ser entre 4 y 15 caracteres entre letras, números y '_'")