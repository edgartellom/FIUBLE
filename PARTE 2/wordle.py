import time
from lib import archivo, grafica, juego


RUTA_DB_PALABRAS = "./db/palabras.csv"
RUTAS_CUENTOS = [ "./assets/Cuentos.txt", "./assets/La araña negra - tomo 1.txt", "./assets/Las 1000 Noches y 1 Noche.txt" ]
CFG_DEFECTO = { 'LONGITUD_PALABRA_SECRETA': '7', 'MAXIMO_PARTIDAS': '5', 'REINICIAR_ARCHIV0_PARTIDAS': 'False' }


def obtener_jugadores():
  jugadores = []
  cant_jugadores = len(jugadores)
  print("Esperando que los jugadores inicien sesión...")
  while cant_jugadores < 2:
    jugador = grafica.solicitar_credenciales(cant_jugadores + 1)
    if jugador != ['', '']:
      jugadores.append(jugador[0])
      cant_jugadores = len(jugadores)
  juego.limpiar_pantalla()
  return jugadores

def actualizar_diccionario(diccionario1, diccionario2):
  diccionario_final = diccionario1
  lista_omisiones = []
  for clave in diccionario2:
    if not clave in diccionario1:
      lista_omisiones.append(clave)
      diccionario_final[clave] = diccionario2[clave]
  
  return diccionario_final, lista_omisiones

def generar_palabras_secretas(config):
  db_palabras = open(RUTA_DB_PALABRAS, "w")
  palabras = archivo.combinar_cuentos(RUTAS_CUENTOS, config["LONGITUD_PALABRA_SECRETA"])
  for palabra in sorted(palabras.keys()):
    db_palabras.write(f'{palabra},{",".join([str(i) for i in palabras[palabra]])}\n')
  db_palabras.close()
  return list(palabras)

def imprimir_configuracion(configuracion, valores_omision):
  print("Configuración del juego")
  for ajuste in configuracion:
    linea = "- " + ajuste + ": " + configuracion[ajuste]
    if ajuste in valores_omision:
      linea += " (omision)"
    print(linea)
  print("\n")

def tiempo_espera(cantidad, intervalo):
  print("El juego está a punto de iniciar", end='', flush=True)
  intervalos = 0
  while intervalos < cantidad:
    time.sleep(intervalo)
    print(".", end='', flush=True)
    intervalos += 1
  print("\n")
  time.sleep(intervalo)



config_archivo = archivo.procesar("./configuracion.csv")
config, omision = actualizar_diccionario(config_archivo, CFG_DEFECTO)

juego.limpiar_pantalla()

jugadores = obtener_jugadores()

imprimir_configuracion(config, omision)
tiempo_espera(3, 1.5)

palabras = generar_palabras_secretas(config)
if (config["REINICIAR_ARCHIV0_PARTIDAS"] == "True"):
  archivo.vaciar("./db/partidas.csv")

juego.juego(jugadores, palabras, config)  