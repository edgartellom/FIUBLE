import time
from lib import archivo, grafica, juego



RUTA_DB_PALABRAS = "./db/palabras.csv"
RUTAS_CUENTOS = [ "./assets/Cuentos.txt", "./assets/La araña negra - tomo 1.txt", "./assets/Las 1000 Noches y 1 Noche.txt" ]
CFG_DEFECTO = { 'LONGITUD_PALABRA_SECRETA': '7', 'MAXIMO_PARTIDAS': '5', 'REINICIAR_ARCHIV0_PARTIDAS': 'False' }






def obtener_jugadores():
	'''
		Instancia la ventana para introducir credenciales
		por cada jugador y retorna una lista con los nombres
		una vez terminado el inicio de sesión de ambos

		~ Tomas Fernández Moreno
	'''

	jugadores = []
	cant_jugadores = len(jugadores)
	print("Esperando que los jugadores inicien sesión...")

	# Mientras que no hayan 2 jugadores...
	while cant_jugadores < 2:

		# Solicita las credenciales
		jugador = grafica.solicitar_credenciales(cant_jugadores + 1)

		# Si son válidas añade el jugador al listado
		if jugador != ['', '']:
			jugadores.append(jugador[0])
			cant_jugadores = len(jugadores)

	juego.limpiar_pantalla()
	return jugadores



def actualizar_diccionario(diccionario1, diccionario2):
	'''
		Añade al diccionario1 las claves que no estén presentes
		en el diccionario2. Retorna el diccionario final junto a
		un listado de las claves que se establecieron acá

		~ Edgar Tello Meléndez
	'''

	diccionario_final = diccionario1
	lista_omisiones = []

	# Para todas las claves del diccionario 2 que NO
	# estén en el diccionario 1
	for clave in diccionario2:
		if not clave in diccionario1:

			# Añade la clave a la lista de valores dados
			# por omisión y la entrada al diccionario final
			lista_omisiones.append(clave)
			diccionario_final[clave] = diccionario2[clave]
	
	return diccionario_final, lista_omisiones



def generar_palabras_secretas(config):
	'''
		Lee la información de los cuentos y las combina en
		el archivo palabras.csv. Una vez hecho eso retorna
		un listado con todas las palabras utilizables

		~ Bruno Ferreyra
	'''
	
	# Obtiene el diccionario de palabras con sus repeticiones
	palabras = archivo.combinar_cuentos(RUTAS_CUENTOS, config["LONGITUD_PALABRA_SECRETA"])

	# Escibe todas las palabras en el archivo palabras.csv
	db_palabras = open(RUTA_DB_PALABRAS, "w")
	for palabra in sorted(palabras.keys()):
		db_palabras.write(f'{palabra},{",".join([str(i) for i in palabras[palabra]])}\n')
	db_palabras.close()

	# Convierte el diccionario de palabras a una lista y lo retorna
	return list(palabras)



def imprimir_configuracion(configuracion, valores_omision):
	'''
		Recibe un diccionario e imprime cada entrada aclarando
		que valores fueron dados por omisión según el listado
		correspondiente

		~ Bruno Ferreyra
	'''

	print("Configuración del juego")

	# Para cada entrada imprime en el formato
	# - [CLAVE]: [VALOR]
	for ajuste in configuracion:
		linea = "- " + ajuste + ": " + configuracion[ajuste]
		if ajuste in valores_omision:
			linea += " (omision)"
		print(linea)
	print("\n")



def tiempo_espera(cantidad, intervalo):
	'''
		Muestra un mensaje de espera al usuario. El objetivo
		de esta función es darle un tiempo al jugador para
		que pueda leer las configuraciones

		~ Bruno Ferreyra
	'''
	
	print("El juego está a punto de iniciar", end='', flush=True)
	intervalos = 0

	# Espera un intervalo dado una cierta
	# cantidad de veces, añadiendo un . al
	# string previo
	while intervalos < cantidad:
		time.sleep(intervalo)
		print(".", end='', flush=True)
		intervalos += 1
	print("\n")
	time.sleep(intervalo)






# Obtener y procesar configuración
config_archivo = archivo.procesar("./configuracion.csv")
config, omision = actualizar_diccionario(config_archivo, CFG_DEFECTO)

# Limpia la pantalla para que la interfaz del juego
# quede sin el historial de la consola
juego.limpiar_pantalla()

# Pedir inicio de sesión de jugadores
jugadores = obtener_jugadores()

# Muestra la configuración y da un tiempo de espera para leer
imprimir_configuracion(config, omision)
tiempo_espera(3, 1.5)

# Obtiene el listado de palabras utilizables según la configuración
palabras = generar_palabras_secretas(config)

# Vacía el archivo de partidas en caso de que así esté configurado
if (config["REINICIAR_ARCHIV0_PARTIDAS"] == "True"):
  	archivo.vaciar("./db/partidas.csv")

# Ejecuta la instancia del juego
juego.juego(jugadores, palabras, config)
