import random
import time
import math
import sys
import os
from datetime import datetime
from . import utiles, cadenas, archivo



# Constantes
INTENTOS_MAXIMOS = 5
PUNTAJE_POR_INTENTOS = {0: 50, 1: 40, 2: 30, 3: 20, 4: 10, 5: -100}
RUTA_ARCHIVO_PARTIDAS = sys.path[0] + "/db/partidas.csv"



#Indices de jugador
JUGADOR_1 = 0
JUGADOR_2 = 1






def cambio_de_turno(turno_actual):
    ''' 
        Al finalizar la partida se llama a esta funcion
        para cambiar el turno 

        ~ María Rosa Ferrara
    '''

    return JUGADOR_2 if turno_actual == JUGADOR_1 else JUGADOR_1



def guardar_puntaje(puntaje, ultimo_turno, turno_actual):
    '''
        Retorna una tupla con los puntajes correspondientes
        a cada jugador dependiendo de cual fue el ganador o
        de si ambos perdieron

        - Índice 0: jugador 1
        - Índice 1: jugador 2

        ~ Tomas Fernández Moreno
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

    return (jugador1punt, jugador2punt)



def limpiar_pantalla():
    '''
        Nada que aclarar acá :p

        ~ Bruno Ferreyra
    '''

    os.system('cls' if os.name == 'nt' else 'clear')



def preguntar_jugar_de_nuevo():
    '''
        Solicita al jugador que ingrese S (si) o N (no)
        dependiendo de si desea seguir jugando

        ~ María Rosa Ferrara
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

        ~ Tomas Fernández Moreno
    '''

    # Obtiene los datos resultantes de la partida
    ultimo_turno = resultado["ultimo_turno"]
    minutos_de_juego = resultado["minutos_de_juego"]
    segundos = resultado["segundos_de_juego"] - (minutos_de_juego * 60)
    puntaje_jugador = resultado["puntaje_jugador"]

    # Obtiene los índices de los jugadores
    ganador = JUGADOR_1 if ultimo_turno == JUGADOR_1 else JUGADOR_2
    perdedor = JUGADOR_2 if ultimo_turno == JUGADOR_1 else JUGADOR_1

    print("\n-----\n")
    print(f"Ganaste {nombres[ganador]}! Tardaste {minutos_de_juego} minutos y {segundos} segundos en adivinar la palabra.\n")
    print(f"Obtuviste un total de {puntaje_jugador} puntos, tenes acumulados {puntos[ganador]} puntos.")
    print(f"El jugador {nombres[perdedor]} perdió un total de {puntaje_jugador} puntos, tenes acumulados {puntos[perdedor]}.")
    print("\n-----\n")



def imprimir_perdedores(nombres, puntos, resultado, primer_turno):
    '''
        Imprime el resumen mostrando cuantos puntos
        perdió cada jugador según cual haya sido el
        primero

        ~ Nicolás Cozza
    '''

    # Obtiene cual jugador se va a imprimir primero
    # dependiendo del primer turno
    primero = primer_turno
    segundo = JUGADOR_1 if primer_turno == JUGADOR_2 else JUGADOR_2
    
    # Extrae la palabra a adivinar del resultado
    palabra_secreta = resultado["palabra_secreta"]

    print("\n-----\n")
    print(f"Perdieron! La palabra era {palabra_secreta}.\n")
    print(f"El jugador {nombres[primero]} perdió un total de 100 y tiene acumulado {puntos[primero]}")
    print(f"Y el jugador {nombres[segundo]} perdió un total de 50 y tiene un total de {puntos[segundo]}")
    print("\n-----\n")



def imprimir_resultados(nombres, puntos, resultado, primer_turno):
    '''
        Muestra los resultados de la partida actual para
        cada jugador desplegando puntajes, pérdidas y
        ganancias de puntos y tiempo empleado en esa ronda

        Al finalizar pregunta si se quiere volver a jugar
        otra partida

        ~ Nicolás Cozza
    '''

    # Extrae el bool de si alguien ganó
    hay_ganador = resultado["gano"]
    
    # Imprime el resultado de la partida
    if hay_ganador:
        imprimir_ganador(nombres, puntos, resultado)
    else:
        imprimir_perdedores(nombres, puntos, resultado, primer_turno)



def analizar_input(palabra, arriesgo):
    '''
        Retorna una tupla con el siguiente formato:
        - es_igual: booleano que determina si las palabras son iguales
        - es_palabra_valida: booleano que determina si el arriesgo es válido
        - mensaje: un mensaje explicitando algún error

        ~ Edgar Tello
    '''

    mensajes = []
    es_palabra_valida = True
    
    # Valida que los caracteres sean correctos
    if not arriesgo.isalpha() and arriesgo != "":
        mensajes.append(f"La palabra {arriesgo} es inválida. No debe contener caracteres especiales ni numéricos.")
        es_palabra_valida = False

    # Se mide si la longitud está bien
    if len(palabra) != len(arriesgo):
        mensajes.append("Largo de la palabra incorrecto")
        es_palabra_valida = False
            
    
    return { \
    "es_igual": palabra == arriesgo, \
    "es_palabra_valida": es_palabra_valida, \
    "mensajes": mensajes \
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

        ~ Edgar Tello
    '''

    texto_con_colores = ""
    texto_sin_colores = ""
    indices_con_coincidencias = []
    indice = 0

    validacion = analizar_input(palabra, arriesgo)
    es_palabra_valida = validacion["es_palabra_valida"]

    while(indice < len(arriesgo) and es_palabra_valida):

        # Normaliza la letra
        letra_arriesgo_normalizada = cadenas.formatear_letra(arriesgo[indice])

        # Si la letra es la misma en la misma posición para
        # las dos palabras, añade el color verde
        if letra_arriesgo_normalizada == palabra[indice]:
            texto_con_colores += utiles.obtener_color("Verde")
            indices_con_coincidencias.append(indice)

        # De otro modo, si la letra simplemente está en la palabra
        # (aunque no en la misma posición), asigna el color amarillo
        elif letra_arriesgo_normalizada in palabra:
            texto_con_colores += utiles.obtener_color("Amarillo")

        # Caso contrario, la letra no se encuentra en la palabra
        # así que se asigna color gris oscuro
        else:
            texto_con_colores += utiles.obtener_color("GrisOscuro")

        # Teniendo el color asignado, colocamos la letra
        texto_con_colores += letra_arriesgo_normalizada
        texto_sin_colores += letra_arriesgo_normalizada

        indice += 1

    # Volvemos a poner el color por defecto para que las
    # siguientes líneas no queden mal
    texto_con_colores += utiles.obtener_color("Defecto")

    return { \
    "texto_con_colores": texto_con_colores, \
    "indices_con_coincidencias": indices_con_coincidencias, \
    }



def imprimir_progreso(palabra_secreta, palabra_revelada):
    '''
        Construye el string de la palabra a adivinar
        dependiendo de las coincidencias que haya en los
        listados

        ~ Bruno Ferreyra
    '''

    progreso_palabra = ""
    for indice, letra in enumerate(palabra_secreta):
        if palabra_revelada[indice] == True:
            progreso_palabra += letra
        else:
            progreso_palabra += "?"

    print("Palabra a adivinar: " + progreso_palabra)



def imprimir_intentos(palabra_secreta, palabras_intentadas):
    '''
        Imprime todas las palabras intentadas por el jugador

        ~ Bruno Ferreyra
    '''

    for indice_intento in range(5):
        if (indice_intento < len(palabras_intentadas)):
            print(palabras_intentadas[indice_intento])
        else:
            print("?" * len(palabra_secreta))



def imprimir_salida_analisis(palabra_analizada, palabra_revelada):
    '''
        Imprime con colores la palabra que arriesgó
        y actualiza los índices de las coincidencias
        encontradas

        ~ Bruno Ferreyra
    '''

    print("Palabra arriesgada: " + palabra_analizada["texto_con_colores"])
    for indice_coincidencia in palabra_analizada["indices_con_coincidencias"]:
        palabra_revelada[indice_coincidencia] = True



def imprimir_errores_analisis(analisis):
    print("\nSe encontraron los siguientes errores:")
    for mensaje in analisis["mensajes"]:
        print(f'- {mensaje}')
    input("\nPresioná enter para continuar...")



def partida(jugadores, turno_actual, palabras_para_adivinar):
    '''
        Instancia una partida y retorna un diccionario
        con datos sobre el resultado

        ~ Bruno Ferreyra
    '''
    
    # Obtiene la palabra para adivinar
    palabra_secreta = random.choice(palabras_para_adivinar)

    # Listado de palabras introducidas por el jugador
    palabras_intentadas = []

    # Listado de índices de la palabra descubiertos
    palabra_revelada = [False for x in range(len(palabra_secreta))]

    intentos_totales = 0
    intentos_jugador = [0, 0]
    aciertos_jugador = [0, 0]
    gano = False

    # Inicia el conteo de tiempo desde el segundo acutal en
    # el sistema epoch (UNIX)
    tiempo_inicial = time.time()

    while (intentos_totales < INTENTOS_MAXIMOS and gano == False):

        limpiar_pantalla()

        # Imprime el progreso de la palabra y todos los intentos
        imprimir_progreso(palabra_secreta, palabra_revelada)
        imprimir_intentos(palabra_secreta, palabras_intentadas)

        # Imprime un mensaje que indica de quien es el turno
        print(f"Es el turno del jugador {jugadores[turno_actual]}")
        
        # Solicita una entrada de una palabra y la analiza
        arriesgo = cadenas.formatear_palabra(input("Arriesgo: "))
        palabra_analizada = pintar_arriesgo(palabra_secreta, arriesgo)
        analisis = analizar_input(palabra_secreta, arriesgo)

        if analisis["mensajes"]:
            imprimir_errores_analisis(analisis)
        else: 
            aciertos = len(palabra_analizada["indices_con_coincidencias"])
            if (aciertos > aciertos_jugador[turno_actual]):
                aciertos_jugador[turno_actual] = aciertos

            # La añade al listado de palabras arriesgadas
            palabras_intentadas.append(palabra_analizada["texto_con_colores"])

            imprimir_salida_analisis(palabra_analizada, palabra_revelada)

            # Si la palabra coincide perfectamente con la palabra a
            # adivinar, se gana el juego
            if (analisis["es_igual"]):
                gano = True

            # Caso contrario, simplemente se cambia de turno
            else:
                intentos_jugador[turno_actual] += 1
                turno_actual = cambio_de_turno(turno_actual)
                
            # Asigna el puntaje correspondiente dependiendo
            # de los intentos
            puntaje_jugador = PUNTAJE_POR_INTENTOS[intentos_totales]

            intentos_totales += 1
            time.sleep(1)
        
    # En caso de que ambos hayan perdido asigna los puntos
    # negativos correspondientes
    if gano == False:    
        puntaje_jugador = PUNTAJE_POR_INTENTOS[intentos_totales]

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
    "intentos_totales": intentos_totales, \
    "palabra_secreta": palabra_secreta, \
    "puntaje_jugador": puntaje_jugador, \
    "ultimo_turno": turno_actual, \
    "jugador": jugadores[turno_actual], \
    "intentos_jugador" : intentos_jugador, \
    "aciertos_jugador": aciertos_jugador
    }



def generar_registro_partida(resultado, jugadores, indice_jugador, fecha):
    '''
        Retorna un string con la información a registrar
        de una partida según la consigna de la etapa 9

        ~ Edgar Tello
    '''

    dia = fecha.strftime("%d/%m/%Y")
    hora = fecha.strftime("%H:%M:%S")
    jugador = jugadores[indice_jugador]
    aciertos = str(resultado["aciertos_jugador"][indice_jugador])
    intentos = resultado["intentos_jugador"][indice_jugador]
    return f'{dia},{hora},{jugador},{aciertos},{intentos}\n'



def registrar_partida(resultado, jugadores):
    '''
        Genera los registros de la partida para cada jugador
        y los escribe en el archivo partidas.csv ordenando
        por cantidad de aciertos

        ~ Tomas Fernández Moreno
    '''

    ahora = datetime.now()

    registro_jugador1 = generar_registro_partida(resultado, jugadores, JUGADOR_1, ahora)
    registro_jugador2 = generar_registro_partida(resultado, jugadores, JUGADOR_2, ahora)

    registros = archivo.obtener_lineas(RUTA_ARCHIVO_PARTIDAS)
    registros.append(registro_jugador1)
    registros.append(registro_jugador2)
    registros.sort(key=lambda x: x.split(',')[3], reverse=True)

    archivo.sobreescribir(RUTA_ARCHIVO_PARTIDAS, registros)



def imprimir_resumen(partidas):
    '''
        Imprime en pantalla un resumen del juego en
        una tabla siendo cada fila la información de
        una partida

        ~ Bruno Ferreyra
    '''

    def alinear_item(string):
        '''
            Añade los espacios en blanco necesarios
            para alinear el texto a la tabla

            ~ Bruno Ferreyra
        '''
        
        return string + "".join([" " for x in range(18 - len(string))])

    print("===================== SINOPSIS DEL JUEGO =====================")
    print("Partida           Palabra           Ganador           Intentos")
    for indice, partida in enumerate(partidas):
        nro_partida = alinear_item(str(indice + 1))
        palabra = alinear_item(partida["palabra_secreta"])
        ganador = alinear_item(partida["jugador"] if partida["gano"] else "-")
        intentos = alinear_item(str(partida["intentos_totales"]))
        print(f'{nro_partida}{palabra}{ganador}{intentos}')
    print("\n")



def juego(jugadores, palabras, config):
    '''
        Instancia el juego

        ~ Bruno Ferreyra
    '''

    # Variables que contendrán los puntajes de cada jugador
    puntos = [0, 0]

    # Establece el turno de uno de los jugadores de manera
    # aleatoria
    turno = random.randint(0,1)

    partidas = []
                            
    # Ciclo del juego
    juego_activo = True
    partidas_jugadas = 0
    while juego_activo:

        limpiar_pantalla()

        # Obtiene los resultados de la partida
        resultado = partida(jugadores, turno, palabras)

        # Registra el resultado de la partida en el listado
        partidas.append(resultado)

        # Genera los puntajes correspondientes para cada
        # jugador en formato de tupla
        puntajes_finales = guardar_puntaje(resultado["puntaje_jugador"],resultado["ultimo_turno"],turno) 

        # Acumula los puntajes obtenidos por cada jugador
        puntos[JUGADOR_1] += puntajes_finales[JUGADOR_1]
        puntos[JUGADOR_2] += puntajes_finales[JUGADOR_2]

        # Muestra los resultados de la partida y los escribe
        # en el archivo correspondiente
        imprimir_resultados(jugadores, puntos, resultado, turno)
        registrar_partida(resultado, jugadores)

        # Cambia de turno
        turno = cambio_de_turno(turno)

        partidas_jugadas += 1

        # Pregunta si se quiere jugar de nuevo
        if partidas_jugadas < int(config["MAXIMO_PARTIDAS"]):
            juego_activo = preguntar_jugar_de_nuevo()
        else:
            juego_activo = False

    limpiar_pantalla()
    imprimir_resumen(partidas)
