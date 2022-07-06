from . import archivo
import sys





def nombre_valido(nombre):
    '''
        Corrobora que el nombre argumentado cumpla
        con las condiciones dadas en la consigna y
        retorna un booleano con la validación

        ~ Edgar Tello
    '''

    registro = archivo.procesar(sys.path[0] + "/db/usuarios.csv")
    valido = True

	# Corrobora que no estén en el registro y que
	# el largo sea correcto
    if nombre not in registro.keys():
        if len(nombre) >= 4 and len(nombre) <= 15:
           indice = 0

		   # Se fija si todos los caracteres son válidos
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
	'''
        Determina que una contraseña sea válida
        según lo consignado y retorna un booleano
        con la validación

        ~ Edgar Tello
	'''

	acentos = ["á", "Á", "é", "É", "í", "Í", "ó", "Ó", "ú", "Ú"]
	valido = True

	# Se asegura que el largo sea correcto
	if len(clave) >= 8 and len(clave) <= 12:

		# Variables de control para almacenar
		# la cantidad de veces que aparecen
		# caracteres de cada tipo
		indice = 0
		mayusculas = 0
		minusculas = 0
		numeros = 0
		guiones = 0
        
		while valido and indice < len(clave):
			caracter = clave[indice]

			if caracter in acentos:
				valido = False
			elif caracter.isupper():
				mayusculas += 1
			elif caracter.islower():
				minusculas += 1
			elif caracter.isnumeric():
				numeros += 1
			elif caracter == "_" or caracter == "-":
				guiones += 1
			indice += 1

		# Si no todas las condiciones están dadas
		# invalida la contraseña
		if not mayusculas > 0 and not minusculas > 0 and not numeros > 0 and not guiones > 0:
			valido = False

	else:
		valido = False
    
	return valido



def registrar_usuario(nombre, clave):
    '''
        Escribe la información de un usuario
        en el archivo usuarios.csv

        ~ Bruno Ferreyra
    '''

    archivo.escribir(sys.path[0] + "/db/usuarios.csv", ",".join([nombre, clave]))



def iniciar_sesion(usuario, clave):
    '''
        Corrobora si el usuario argumentado existe
        en el archivo usuarios.csv y en ese caso
        verifica que la clave sea correcta. Retorna
        un booleano en caso de que la operación sea
        exitosa

        ~ Tomas Fernández Moreno
    '''

    sesion_iniciada = False
    registro = archivo.procesar(sys.path[0] + "/db/usuarios.csv")
    if usuario in registro and clave == registro[usuario]:
        sesion_iniciada = True

    return sesion_iniciada