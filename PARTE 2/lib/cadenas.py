REEMPLAZOS_TILDES = { "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U" }

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