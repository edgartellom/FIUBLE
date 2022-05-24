import random
import time
import math
from utiles import *
INTENTOS_MAXIMOS = 5
REEMPLAZOS_TILDES = { "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u" }


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
        if not arriesgo[indice].isalpha() or arriesgo[indice].isnumeric():    #es necesario el isnumeric?
        #if not arriesgo[indice].isalpha():
            mensaje = "El caracter \"" + arriesgo[indice] + "\" es inválido"
            #mensaje = "La palabra es inválida. No se permiten números ni caracteres especiales"
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


def raiz():

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

        intentos += 1

    # Obtiene el tiempo final siguiendo la misma metodología de antes
    tiempo_final = time.time()

    if gano:
        segundos_de_juego = int(tiempo_final - tiempo_inicial)
        minutos_de_juego = math.floor(segundos_de_juego / 60)
        print(f"Ganaste! Tardaste {minutos_de_juego} minutos y {segundos_de_juego - (minutos_de_juego * 60)} segundos en adivinar la palabra")
    else:
        print(f"Perdiste! La palabra era {palabra_a_adivinar}")

raiz()
