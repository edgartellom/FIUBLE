import random
import time
import math
from utiles import *

INTENTOS_MAXIMOS = 5
REEMPLAZOS_TILDES = { "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u" }


#------------control de dos jugadores-------------------------#

def dos_jug():
    jug_1 = input("Ingrese el nombre del jugador 1: ")
    jug_2 = input("Ingrese el nombre del jugador 2: ")
    return jug_1 , jug_2

def turno():
    turno = random.randint(0,1)
    return turno

def cambio_de_turno(turno_inicial):
    """ 
        Al finalizar la partida se llama a esta funcion para cambiar el turno 
    """
    if turno_inicial == 0:
        turno_inicial = 1
    else:
        turno_inicial = 0
    return turno_inicial

#---------------------------control de puntaje-----------------#

# Defino estas variables para que por mediante funciones acumule los puntajes de cada jugador 
Jugador1_punt= 0
Jugador2_punt= 0


def sistema_puntaje(intentos):
    """
    Esta funcion tiene un diccionario con la relacion de intentos y puntos
    devolviendo el valor correspondiente 
    """
    valor_puntaje = {0:50,1:40,2:30,3:20,4:10,5:-100} 
    return valor_puntaje[intentos]



def guardar_puntaje (puntaje,turno,turno_inicial):

    """
        Esta funcion dependiendo de quien fue el ganador o si ambos perdieron, le asigna su puntaje correspondiente y 
        regresa una tupla de dos numeros, uno para cada jugador. 
    """

    jugador1punt = 0    # Declarando variables

    jugador2punt = 0
                        # En el caso de si alguno de los dos gano
    if turno == 0:
        jugador1punt = puntaje
        jugador2punt = - puntaje
    else:
        jugador2punt = puntaje
        jugador1punt = - puntaje
                                # En el caso de que ambos perdieron
    if puntaje == -100:
        if turno_inicial == 0:
            jugador1punt = puntaje
            jugador2punt =  round(puntaje / 2)
        else:
            jugador2punt = puntaje
            jugador1punt = round(puntaje / 2)
    return(jugador1punt,jugador2punt)
    

#-----------------------control del juego----------------------------#

# variable de control para el ciclo del juego

juego_ = True 

def game_over(gano,minutos_de_juego,segundos_de_juego,palabra_a_adivinar,puntaje_jugador,turno_inicial, ultimo_turno, nombres,puntos_del_jug1,puntos_del_jug2):

    """
        Esta funcion recibe los resultados del juego actual y muestra al jugador su puntaje final y total
        y al final le pregunta si quiere volver a jugar
    """
    if gano:
        if ultimo_turno == 0:
            print (f"\nGanaste {nombres [ultimo_turno]} Tardaste {minutos_de_juego} minutos y {segundos_de_juego - (minutos_de_juego * 60)} segundos en adivinar la palabra\n")
            print(f"Obtuviste un total de {puntaje_jugador} puntos, tenes acumulados {puntos_del_jug1} puntos")
            print(f"EL jugador {nombres[1]} perdio un total de {puntaje_jugador} puntos, tenes acumulados {puntos_del_jug2}\n")
        else:
            print (f"\nGanaste {nombres [ultimo_turno]} Tardaste {minutos_de_juego} minutos y {segundos_de_juego - (minutos_de_juego * 60)} segundos en adivinar la palabra\n")
            print(f"Obtuviste un total de {puntaje_jugador} puntos, tenes acumulados {puntos_del_jug2} puntos")
            print(f"EL jugador {nombres[0]} perdio un total de {puntaje_jugador} puntos, tenes acumulados {puntos_del_jug1}\n")
       # print(f"Ganaste! Tardaste {minutos_de_juego} minutos y {segundos_de_juego - (minutos_de_juego * 60)} segundos en adivinar la palabra")
       # print()
       # print(f"Obtuviste un total de {puntaje_jugador} puntos,tenes acumulados {puntaje_total_jug}")
    else:
        #puntaje_jugador = sistema_puntaje(intentos)
    
        print(f"\nPerdieron! La palabra era {palabra_a_adivinar}")
        print()
        if turno_inicial == 0:
            print(f"El jugador {nombres[turno_inicial]} perdio un total de 100 y tiene acumulado {puntos_del_jug1}")
            print(f"Y el jugador {nombres[1]} perdio un total de 50 y tiene un total de {puntos_del_jug2}\n")
        else:
            print(f"El jugador {nombres[turno_inicial]} perdio un total de 100 y tiene acumulado {puntos_del_jug2}")
            print(f"Y el jugador {nombres[0]} perdio un total de 50 y tiene un total de {puntos_del_jug1}\n")
        #print(f"Perdiste un total de 100 puntos, tenes acumulados {puntaje_total_jug}")

    pregunta =""
    juego = False
    while (pregunta != "S") and (pregunta != "N"):
        pregunta = input("Desea jugar otra pratida? S/N: ").upper()
        
    if pregunta == "S":

        juego = True

    return juego


#-----------------control de letras-------------------------#

def formatear_letra(letra):
    '''
    Devuelve una letra dada en mayúscula y sin tilde
    '''
    letra_formateada = letra

    # Evalúa si la letra está en el diccionario de
    # tildes y le asigna su par sin tilde
    if letra in REEMPLAZOS_TILDES:
        letra_formateada = REEMPLAZOS_TILDES[letra]

    # Convierte la letra a mayúscula
    letra_formateada = letra_formateada.upper()

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
    Realiza una iteración letra a letra a los efectos de
    darles color dependiendo de la posición de cada una.

    Si la letra existe en las dos palabras y se encuentra
    en la misma posición, le asigna el color VERDE

    Si la letra existe en las dos palabras y NO está en
    la misma posición, le asigna el color AMARILLO

    Si la letra no existe en la otra palabra, le asigna
    GRIS OSCURO

    Retorna una tupla con el siguiente formato:
    Índice 0: palabra con colores
    Índice 1: booleano que determina si las palabras son iguales
    Índice 2: un mensaje explicitando algún error
    '''

    mensaje = ""
    es_palabra_valida = True
    texto_con_colores = ""
    texto_sin_colores = ""
    indices_con_coincidencias = []

    # Primero, medimos si la longitud de las palabras coinciden
    if len(palabra) != len(arriesgo):
        mensaje = "La palabra debe ser de 5 letras"
        es_palabra_valida = False

    # Realiza una iteración letra por letra teniendo en cuenta
    # la posición de la misma
    indice = 0
    while(indice < len(arriesgo) and es_palabra_valida):

        # Valida que la letra no sea un caracter especial o numérico
        if not arriesgo[indice].isalpha():
            mensaje = "El caracter \"" + arriesgo[indice] + "\" es inválido"
            es_palabra_valida = False

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
    "es_igual": palabra == texto_sin_colores, \
    "indices_con_coincidencias": indices_con_coincidencias, \
    "mensaje": mensaje \
    }

#-----------------control del juego------------------------#

def raiz(jugadores,turn_actu):
    
    # Obtiene una palabra aleatoria de la lista y la normaliza
    palabras_para_adivinar = obtener_palabras_validas()
    indice_palabra = random.randint(0, len(palabras_para_adivinar) - 1)
    palabra_a_adivinar = formatear_palabra(palabras_para_adivinar[indice_palabra])

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

        # Imprime todas las palabras intentadas por el jugador
        for indice_intento in range(5):
            if (indice_intento < len(palabras_intentadas)):
                print(palabras_intentadas[indice_intento])
            else:
                print("?" * len(palabra_a_adivinar))

        # Solicita una entrada de una palabra y la analiza
        if turn_actu == 0:
            print(f"Es el turno del jugador {jugadores[turn_actu]}")
        else:
            print(f"Es el turno del jugador {jugadores[turn_actu]}")

        arriesgo = input("Arriesgo: ")
        palabra_analizada = analizar_input(palabra_a_adivinar, arriesgo)

        # La añade al listado de palabras arriesgadas
        palabras_intentadas.append(palabra_analizada["texto_con_colores"])

        # Si la palabra ingresada por el jugador no de ningún
        # problema, imprime con colores la palabra que arriesgó,
        # y actualiza los índices de las coincidencias encontradas
        if palabra_analizada["mensaje"] == "":
            print("Palabra arriesgada: " + palabra_analizada["texto_con_colores"])
            for indice_coincidencia in palabra_analizada["indices_con_coincidencias"]:
                palabra_revelada[indice_coincidencia] = True

        # Caso contrario, imprime el problema que tiene esa palabra
        else:
            print(palabra_analizada["mensaje"])

        # Si la palabra coincide perfectamente con la palabra a
        # adivinar, se gana el juego
        if (palabra_analizada["es_igual"] == True):
            gano = True
        else:                   #Si no adivino la palabra cambia de turno
            if turn_actu == 0:
                turn_actu = 1
            else:
                turn_actu = 0  

        #asigna el puntaje dependiendo de los intentos

        puntaje_jugador = sistema_puntaje(intentos)

        intentos += 1
        

    # esta condicion garantiza que al perder te de el puntaje correspondiente
    if gano == False:    
        puntaje_jugador = sistema_puntaje(intentos)

    # Obtiene el tiempo final siguiendo la misma metodología de antes
    tiempo_final = time.time()
    segundos_de_juego = int(tiempo_final - tiempo_inicial)
    minutos_de_juego = math.floor(segundos_de_juego / 60)

    # regresar un diccionario con los resultados finales de la partida actual

    return {"gano":gano, "minutos_de_juego":minutos_de_juego, "segundos_de_juego":segundos_de_juego,
    "intentos":intentos,"palabra_a_adivinar":palabra_a_adivinar, "puntaje_jugador":puntaje_jugador, "ultimo_turno":turn_actu}

# inicio del juego

NOMBRES_JUGADORES = dos_jug() #Guarda una tupla con los dos nombres

turno_inicial = turno() #Guarda el valor del primer turno dado,  que despues me va a servir para cambiarla al volver
                        #empezar el juego

while juego_:

    resultado = raiz(NOMBRES_JUGADORES,turno_inicial) # Esta variable guarada el diccionario que regresa la funcion con todos los datos de la partida

    puntajes_finales = guardar_puntaje(resultado["puntaje_jugador"],resultado["ultimo_turno"],turno_inicial) 

    Jugador1_punt += puntajes_finales[0]
    Jugador2_punt += puntajes_finales[1]

    juego_ = game_over(resultado["gano"],resultado["minutos_de_juego"],
        resultado["segundos_de_juego"],resultado["palabra_a_adivinar"],
        resultado["puntaje_jugador"],turno_inicial, resultado["ultimo_turno"], 
        NOMBRES_JUGADORES,Jugador1_punt,Jugador2_punt) 

    turno_inicial = cambio_de_turno(turno_inicial)
