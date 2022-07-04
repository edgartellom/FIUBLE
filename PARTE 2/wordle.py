# from lib.juego import juego
from lib import archivos, grafica, juego

# 1. leer la configuración // HECHO
# 2. Iniciar sesión (o registrar) // HECHO
# 3. según la configuración generar la db con las palabras adecuadas
# 4. iniciar el juego con las palabras correctas y el número de intentos configurado
# 5. repetir en caso de que el usuario desee

RUTA_DB_PALABRAS = "./db/palabras.csv"

RUTAS_CUENTOS = [
  "./assets/Cuentos.txt",
  "./assets/La araña negra - tomo 1.txt",
  "./assets/Las 1000 Noches y 1 Noche.txt"  
]

CFG_DEFECTO = {
  'LONGITUD_PALABRA_SECRETA': '7',
  'MAXIMO_PARTIDAS': '5',
  'REINICIAR_ARCHIV0_PARTIDAS': 'False'
}


def obtener_jugadores():
  jugadores = []
  cant_jugadores = len(jugadores)
  while cant_jugadores < 2:
    jugador = grafica.solicitar_credenciales(cant_jugadores + 1)
    jugadores.append(jugador[0])
    cant_jugadores = len(jugadores)
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
  palabras = archivos.combinar_cuentos(RUTAS_CUENTOS, config["LONGITUD_PALABRA_SECRETA"])
  for palabra in sorted(palabras.keys()):
    db_palabras.write(f'{palabra},{",".join([str(i) for i in palabras[palabra]])}\n')
  db_palabras.close()
  return list(palabras)

def imprimir_configuracion(configuracion, valores_omision):
  print("\n\n\n")
  print("CONFIGURACIÓN DEL JUEGO:")
  for ajuste in configuracion:
    linea = ajuste + ": " + configuracion[ajuste]
    if ajuste in valores_omision:
      linea += " (omision)"
    print(linea)
  print("\n\n")


# Runtime
config_archivo = archivos.procesar_archivo("./configuracion.csv")
config, omision = actualizar_diccionario(config_archivo, CFG_DEFECTO)
#jugadores = obtener_jugadores()

imprimir_configuracion(config, omision)
palabras = generar_palabras_secretas(config)
if (config["REINICIAR_ARCHIV0_PARTIDAS"] == "True"):
  archivos.vaciar_archivo("./db/partidas.csv")

jugadores = ("bruno","tomas")
juego.juego(jugadores, palabras, config)  