import string
from . import cadenas



SEPARADOR_CSV = ","
SEPARADOR_TXT = " "






def leer_linea(archivo, separador, default = ["", ""]):
	'''
		Dada la instancia de un archivo lee una línea
		y la retorna separada según separador especificado

		~ Tomas Fernández Moreno
	'''

	linea = archivo.readline()
	return linea.rstrip("\n").split(separador) if linea else default



def combinar_cuentos(cuentos, longitud_palabras):
	'''
		Retorna un diccionario con la cantidad de veces
		que cada palabra aparece en cada texto.

		Cada clave es una palabra y el valor es un listado
		con tantos índices como cuentos. Estos contendrán
		la cantidad de veces que la palabra haya sido
		encontrada en cada texto (en el mismo orden).

		~ Bruno Ferreyra
	'''

	palabras = {}
	# Para cada texto...
	for indice, cuento in enumerate(cuentos):

		# Lo abre y lee todas las lineas, siendo que
		# para cada una...
		archivo = open(cuento)

		linea = leer_linea(archivo, SEPARADOR_TXT, "")

		while linea:

			#Busca todas las palabras
			for palabra in linea:

				# Limpia la  palabra de caracteres especiales y
				# corrobora que cumpla con las condiciones
				palabra_limpia = palabra.strip(string.punctuation)
				if palabra_limpia.isalpha() and len(palabra_limpia) == int(longitud_palabras):
					
					# Formatea la palabra y revisa que todavía no
					# exista en el diccionario
					palabra_formateada = cadenas.formatear_palabra(palabra_limpia)
					if not palabra_formateada in palabras:
						
						# En caso de que no exista añade el listado
						# con tantos índices como cuentos
						palabras[palabra_formateada] = [0 for x in range(len(cuentos))]
					
					# Añade una unidad en el listado correspondiente
					# a esa palabra en el índice del texto actual
					palabras[palabra_formateada][indice] += 1
			linea = leer_linea(archivo, SEPARADOR_TXT, "")
		archivo.close()
	
	return palabras



def procesar(ruta_archivo):
	'''
		Lee un archivo y devuelve un diccionario
		con la primera palabra de cada línea como
		clave y la segunda como valor (ignorando
		todo lo demás)

		~ Bruno Ferreyra
	'''

	# Abre el archivo, determina su extensión y
	# establece el separador adecuado
	archivo = open(ruta_archivo, "r")
	extension = archivo.name.split(".")[-1]
	separador = SEPARADOR_CSV if extension == "csv" else SEPARADOR_TXT

	# Lee todas las líneas del archivo y las
	# establece en el registro según lo previamente
	# dicho
	registro = {}
	linea = leer_linea(archivo, separador)
	while linea[0]:
		valor = linea[1:len(linea)]
		registro[linea[0]] = valor[0] if valor else ""
		linea = leer_linea(archivo, separador)

	return registro



def obtener_lineas(ruta_archivo):
	'''
		Devuelve todas las líneas de un archivo
		en una lista

		~ Bruno Ferreyra
	'''

	archivo = open(ruta_archivo)
	lineas = archivo.readlines()
	archivo.close()
	return lineas



def escribir(ruta_archivo, cadena):
	'''
		Añade a un archivo una cadena determinada

		~ Tomas Fernández Moreno
	'''

	archivo = open(ruta_archivo, "a")
	archivo.write(cadena)
	archivo.close()



def sobreescribir(ruta_archivo, contenido):
	'''
		Sobreescribe un archivo con un string
		determinado o con una lista (escribiendo
		una línea por cada índice)

		~ Edgar Tello
	'''

	archivo = open(ruta_archivo, "w")

	# En caso de que sea un lista escribe
	# línea a línea
	if isinstance(contenido, list):
		for linea in contenido:
			archivo.write(linea)

	# Caso contrario, simplemente escribe
	# el string
	else:
		archivo.write(contenido)
			
	archivo.close()



def vaciar(ruta_archivo):
	'''
		Vacía un archivo

		~ Edgar Tello
	'''
	
	archivo = open(ruta_archivo, "w")
	archivo.write("")
	archivo.close()
