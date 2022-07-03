# from lib.juego import juego
from lib import archivos, grafica

# 1. leer la configuración
# 2. Iniciar sesión (o registrar)
# 3. según la configuración generar la db con las palabras adecuadas
# 4. iniciar el juego con las palabras correctas y el número de intentos configurado
# 5. repetir en caso de que el usuario desee

def obtener_jugadores():
  jugadores = []
  cant_jugadores = len(jugadores)
  while cant_jugadores < 2:
    jugador = grafica.solicitar_credenciales(cant_jugadores + 1)
    jugadores.append(jugador[0])
    cant_jugadores = len(jugadores)
  return jugadores


config = archivos.procesar_archivo("./configuracion.csv")
jugadores = obtener_jugadores()

print(jugadores)
# usuarios.iniciar_sesion("./db/usuarios.csv", "Edgar", "T3llo_mel")
# juego()
