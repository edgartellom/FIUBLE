from utiles import *
import random
import time
import math

# Constantes
INTENTOS_MAXIMOS = 5
REEMPLAZOS_TILDES = { "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U" }
PUNTAJE_POR_INTENTOS = {0: 50, 1: 40, 2: 30, 3: 20, 4: 10, 5: -100}

#Indices de jugador
JUGADOR_1 = 0
JUGADOR_2 = 1


#------------control de dos jugadores-------------------------#

def solicitar_nombres_jugadores():
    '''
    Solicita los nombres de los jugadores y los
    retorna empaquetados
    '''

    jug_1 = input("Ingrese el nombre del jugador 1: ")
    jug_2 = input("Ingrese el nombre del jugador 2: ")
    return jug_1, jug_2

def cambio_de_turno(turno_actual):
    ''' 
    Al finalizar la partida se llama a esta funcion
    para cambiar el turno 
    '''

    return JUGADOR_2 if turno_actual == JUGADOR_1 else JUGADOR_1

#---------------------------control de puntaje-----------------#

def guardar_puntaje(puntaje, ultimo_turno, turno_actual):
    '''
    Retorna una tupla con los puntajes correspondientes
    a cada jugador dependiendo de cual fue el ganador o
    de si ambos perdieron

    - Índice 0: jugador 1
    - Índice 1: jugador 2
    '''

    jugador1punt = 0
    jugador2punt = 0
    
    # Si alguno de los dos ganó establece los
    # puntajes adecuados a cada jugador dependiendo
    # de quien haya sido el último turno
    
    if ultimo_turno == JUGADOR_1:
        jugador1punt = puntaje
        jugador2punt = -puntaje
    else:
        jugador2punt = puntaje
        jugador1punt = -puntaje

    # Si ambos perdieron...
    if puntaje == -100:

        # Establece los puntajes correspondientes a cada
        # jugado dependiendo del turno actual. Al jugador
        # del turno actual se le da un puntaje y al otro
        # la mitad
        if turno_actual == JUGADOR_1:
            jugador1punt = puntaje
            jugador2punt = round(puntaje / 2)
        else:
            jugador2punt = puntaje
            jugador1punt = round(puntaje / 2)

    return (jugador1punt,jugador2punt)
    

#-----------------------control del juego----------------------------#

def preguntar_jugar_de_nuevo():
    '''
    Solicita al jugador que ingrese S (si) o N (no)
    dependiendo de si desea seguir jugando
    '''

    # Variable para almacenar la respuesta
    respuesta = ""

    # Solicita que ingrese S o N
    while (respuesta != "S") and (respuesta != "N"):
        respuesta = input("Desea jugar otra partida? S/N: ").upper()

    return respuesta == "S"

def imprimir_ganador(nombres, puntos, resultado):
    '''
    Imprime el resumen mostrando como ganador
    al jugador que haya tenido el último turno
    '''

    # Obtiene los datos resultantes de la partida
    ultimo_turno = resultado["ultimo_turno"]
    minutos_de_juego = resultado["minutos_de_juego"]
    segundos = resultado["segundos_de_juego"] - (minutos_de_juego * 60)
    puntaje_jugador = resultado["puntaje_jugador"]

    # Obtiene los índices de los jugadores
    ganador = JUGADOR_1 if ultimo_turno == JUGADOR_1 else JUGADOR_2
    perdedor = JUGADOR_2 if ultimo_turno == JUGADOR_1 else JUGADOR_1

    print (f"\nGanaste {nombres[ganador]}! Tardaste {minutos_de_juego} minutos y {segundos} segundos en adivinar la palabra.\n")
    print(f"Obtuviste un total de {puntaje_jugador} puntos, tenes acumulados {puntos[ganador]} puntos.")
    print(f"El jugador {nombres[perdedor]} perdió un total de {puntaje_jugador} puntos, tenes acumulados {puntos[perdedor]}.\n")

def imprimir_perdedores(nombres, puntos, resultado, primer_turno):
    '''
    Imprime el resumen mostrando cuantos puntos
    perdió cada jugador según cual haya sido el
    primero
    '''

    # Obtiene cual jugador se va a imprimir primero
    # dependiendo del primer turno
    primero = primer_turno
    segundo = JUGADOR_1 if primer_turno == JUGADOR_2 else JUGADOR_2
    
    # Extrae la palabra a adivinar del resultado
    palabra_a_adivinar = resultado["palabra_a_adivinar"]

    print(f"\nPerdieron! La palabra era {palabra_a_adivinar}.\n")
    print(f"El jugador {nombres[primero]} perdió un total de 100 y tiene acumulado {puntos[primero]}")
    print(f"Y el jugador {nombres[segundo]} perdió un total de 50 y tiene un total de {puntos[segundo]}\n")

def imprimir_resultados(nombres, puntos, resultado, primer_turno):
    '''
    Muestra los resultados de la partida actual para
    cada jugador desplegando puntajes, pérdidas y
    ganancias de puntos y tiempo empleado en esa ronda

    Al finalizar pregunta si se quiere volver a jugar
    otra partida
    '''

    # Extrae el bool de si alguien ganó
    hay_ganador = resultado["gano"]
    
    # Imprime el resultado de la partida
    if hay_ganador:
        imprimir_ganador(nombres, puntos, resultado)
    else:
        imprimir_perdedores(nombres, puntos, resultado, primer_turno)

#-----------------control de letras-------------------------#

def formatear_letra(letra):
    '''
    Devuelve una letra dada en mayúscula y sin tilde
    '''

    letra_formateada = letra

    # Convierte la letra a mayúscula
    if letra_formateada.islower():
        letra_formateada = letra_formateada.upper()

    # Evalúa si la letra está en el diccionario de
    # tildes y le asigna su par sin tilde
    if letra_formateada in REEMPLAZOS_TILDES:
        letra_formateada = REEMPLAZOS_TILDES[letra_formateada]

    return letra_formateada

#-----------------control de palabras-----------------------#

def formatear_palabra(palabra):
    '''
    Devuelve una palabra dada en mayúscula y sin tildes
    '''

    palabra_formateada = ""

    # Itera letra por letra para retornar la palabra
    # formateada 
    for letra in palabra:
        palabra_formateada += formatear_letra(letra)

    return palabra_formateada

#-----------control del ingreso ----------------------------#

def analizar_input(palabra, arriesgo):
    '''
    Retorna una tupla con el siguiente formato:
    - es_igual: booleano que determina si las palabras son iguales
    - es_palabra_valida: booleano que determina si el arriesgo es válido
    - mensaje: un mensaje explicitando algún error
    '''

    mensaje = ""
    es_palabra_valida = True
    

    # Primero, medimos si la longitud de las palabras coinciden
    if len(palabra) != len(arriesgo):
        mensaje = "La palabra debe ser de 5 letras"
        es_palabra_valida = False
    else:
        # Valida que el arriesgo no contenga un caracter especial o numérico
        if not arriesgo.isalpha():
            mensaje = f"La palabra {arriesgo} es inválida. No debe contener caracteres especiales ni numéricos."
            es_palabra_valida = False
    
    return { \
    "es_igual": palabra == arriesgo, \
    "es_palabra_valida": es_palabra_valida, \
    "mensaje": mensaje \
    }

def pintar_arriesgo(palabra, arriesgo):
    '''
    Realiza una iteración letra a letra a los efectos de
    darles color dependiendo de la posición de cada una.

    Si la letra existe en las dos palabras y se encuentra
    en la misma posición, le asigna el color VERDE

    Si la letra existe en las dos palabras y NO está en
    la misma posición, le asigna el color AMARILLO

    Si la letra no existe en la otra palabra, le asigna
    GRIS OSCURO

    Retorna una tupla con el siguiente formato:
    - texto_con_colores: palabra con colores
    - indices_con_coincidencias: indices coincidentes con el arriesgo
    '''

    texto_con_colores = ""
    texto_sin_colores = ""
    indices_con_coincidencias = []
    indice = 0

    validacion = analizar_input(palabra, arriesgo)
    es_palabra_valida = validacion["es_palabra_valida"]

    while(indice < len(arriesgo) and es_palabra_valida):

        # Normaliza la letra
        letra_arriesgo_normalizada = formatear_letra(arriesgo[indice])

        # Si la letra es la misma en la misma posición para
        # las dos palabras, añade el color verde
        if letra_arriesgo_normalizada == palabra[indice]:
            texto_con_colores += obtener_color("Verde")
            indices_con_coincidencias.append(indice)

        # De otro modo, si la letra simplemente está en la palabra
        # (aunque no en la misma posición), asigna el color amarillo
        elif letra_arriesgo_normalizada in palabra:
            texto_con_colores += obtener_color("Amarillo")

        # Caso contrario, la letra no se encuentra en la palabra
        # así que se asigna color gris oscuro
        else:
            texto_con_colores += obtener_color("GrisOscuro")

        # Teniendo el color asignado, colocamos la letra
        texto_con_colores += letra_arriesgo_normalizada
        texto_sin_colores += letra_arriesgo_normalizada

        indice += 1

    # Volvemos a poner el color por defecto para que las
    # siguientes líneas no queden mal
    texto_con_colores += obtener_color("Defecto")

    return { \
    "texto_con_colores": texto_con_colores, \
    "indices_con_coincidencias": indices_con_coincidencias, \
    }

def revelar_progreso(palabra_a_adivinar, palabra_revelada):
    # Construye el string de la palabra a adivinar
    # dependiendo de las coincidencias que haya en los
    # listados
    progreso_palabra = ""
    for indice, letra in enumerate(palabra_a_adivinar):
        if palabra_revelada[indice] == True:
            progreso_palabra += letra
        else:
            progreso_palabra += "?"

    print("\n\nPalabra a adivinar: " + progreso_palabra)

def imprimir_todo_intento(palabra_a_adivinar, palabras_intentadas):
    # Imprime todas las palabras intentadas por el jugador
    for indice_intento in range(5):
        if (indice_intento < len(palabras_intentadas)):
            print(palabras_intentadas[indice_intento])
        else:
            print("?" * len(palabra_a_adivinar))

def imprimir_salida_analisis(analisis, palabra_analizada, palabra_revelada):
    # Si la palabra ingresada por el jugador no da ningún
    # problema, imprime con colores la palabra que arriesgó,
    # y actualiza los índices de las coincidencias encontradas
    if analisis["mensaje"] == "":
        print("Palabra arriesgada: " + palabra_analizada["texto_con_colores"])
        for indice_coincidencia in palabra_analizada["indices_con_coincidencias"]:
            palabra_revelada[indice_coincidencia] = True

    # Caso contrario, imprime el problema que tiene esa palabra
    else:
        print(analisis["mensaje"])

#-----------------control del juego------------------------#

def partida(jugadores,turno_actual):
    
    # Obtiene una palabra aleatoria de la lista y la normaliza
    palabras_para_adivinar = obtener_palabras_validas()
    palabra_random = random.choice(palabras_para_adivinar)
    palabra_a_adivinar = formatear_palabra(palabra_random)
    # Listado de palabras introducidas por el jugador
    palabras_intentadas = []

    # Listado de índices de la palabra descubiertos
    palabra_revelada = [False for x in range(5)]

    intentos = 0
    gano = False

    # Inicia el conteo de tiempo desde el segundo acutal en
    # el sistema epoch (UNIX)
    tiempo_inicial = time.time()

    while (intentos < INTENTOS_MAXIMOS and gano == False):

        revelar_progreso(palabra_a_adivinar, palabra_revelada)  

        imprimir_todo_intento(palabra_a_adivinar, palabras_intentadas)

        #Imprime un mensaje que indica de quien es el turno
        print(f"Es el turno del jugador {jugadores[turno_actual]}")
        
        # Solicita una entrada de una palabra y la analiza
        arriesgo = formatear_palabra(input("Arriesgo: "))
        palabra_analizada = pintar_arriesgo(palabra_a_adivinar, arriesgo)
        analisis = analizar_input(palabra_a_adivinar, arriesgo)

        # La añade al listado de palabras arriesgadas
        palabras_intentadas.append(palabra_analizada["texto_con_colores"])

        imprimir_salida_analisis(analisis, palabra_analizada, palabra_revelada)

        # Si la palabra coincide perfectamente con la palabra a
        # adivinar, se gana el juego
        if (analisis["es_igual"]):
            gano = True

        # Caso contrario, simplemente se cambia de turno
        else:
            turno_actual = cambio_de_turno(turno_actual)

        # Asigna el puntaje correspondiente dependiendo
        # de los intentos
        puntaje_jugador = PUNTAJE_POR_INTENTOS[intentos]

        intentos += 1
        
    # En caso de que ambos hayan perdido asigna los puntos
    # negativos correspondientes
    if gano == False:    
        puntaje_jugador = PUNTAJE_POR_INTENTOS[intentos]

    # Obtiene el tiempo final siguiendo la misma metodología
    # de antes (ms UNIX)
    tiempo_final = time.time()
    segundos_de_juego = int(tiempo_final - tiempo_inicial)
    minutos_de_juego = math.floor(segundos_de_juego / 60)

    # Retorna un diccionario con los resultados finales de la partida actual
    return { \
    "gano": gano, \
    "minutos_de_juego": minutos_de_juego, \
    "segundos_de_juego": segundos_de_juego, \
    "intentos": intentos, \
    "palabra_a_adivinar": palabra_a_adivinar, \
    "puntaje_jugador": puntaje_jugador, \
    "ultimo_turno": turno_actual \
    }


def juego():
    '''
    Instancia el juego
    '''

    # Variables que contendrán los puntajes de cada jugador
    # puntos[JUGADOR_1] = 0
    # puntos[JUGADOR_2] = 0
    puntos = [0, 0]

    # Solicita los nombres de ambos jugadores y los guarda
    # en una tupla
    jugadores = solicitar_nombres_jugadores()

    # Establece el turno de uno de los jugadores de manera
    # aleatoria
    turno = random.randint(0,1)
                            
    # Ciclo del juego
    juego_activo = True
    while juego_activo:

        # Obtiene los resultados de la partida
        resultado = partida(jugadores, turno) 

        # Genera los puntajes correspondientes para cada
        # jugador en formato de tupla
        puntajes_finales = guardar_puntaje(resultado["puntaje_jugador"],resultado["ultimo_turno"],turno) 

        # Acumula los puntajes obtenidos por cada jugador
        puntos[JUGADOR_1] += puntajes_finales[JUGADOR_1]
        puntos[JUGADOR_2] += puntajes_finales[JUGADOR_2]

        # Muestra los resultados de la partida
        imprimir_resultados(jugadores, puntos, resultado, turno)

        # Pregunta si se quiere jugar de nuevo
        juego_activo = preguntar_jugar_de_nuevo()

        # Cambia de turno
        turno = cambio_de_turno(turno)

juego()