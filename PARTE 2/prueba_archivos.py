def leer_archivo():
    lineas = []
    with open("usuarios.csv","r") as archivo:

        linea = archivo.readline().rstrip("\n").split(",")

        while "" not in linea:
            lineas.append(linea)
            linea = archivo.readline().rstrip("\n").split(",")
    
    return lineas

def procesar_archivo():
    lineas = leer_archivo()
    registro = {}
    for linea in lineas:
        nombre, contraseña = linea[0], linea[1]
        registro[nombre] = contraseña

    return registro

def nombre_valido(nombre):
    registro = procesar_archivo()
    valido = True
    if nombre not in registro.keys():
        if len(nombre) >= 4 and len(nombre) <= 15:
           indice = 0
           while valido and indice < len(nombre):
                caracter = nombre[indice]
                if not caracter.isalnum() and not caracter == "_":
                    valido = False
                indice +=1
        else:
            valido = False
    else:
        valido = False
    return valido

def contraseñas_iguales(contra1_contra2):
    valido = False
    if contra1 == contra2:
        valido = True
        contra = contra2
    return {es_valido:valido, contraseña:contra}

def contraseña_valida(contraseña):
    acentos = [á, Á, é, É, í, Í, ó, Ó, ú, Ú]
    valido = True
    if len(contraseña) >= 8 and len(contraseña) <= 12:
        indice = 0
        mayusculas = 0
        minusculas = 0
        numeros = 0
        guiones = 0
        while valido and indice < len(contraseña):
            caracter = contraseña[indice]
            if caracter.isupper():
                mayusculas += 1
            elif caracter.islower():
                minusculas += 1
            elif caracter.isdigit():
                numeros += 1
            elif caracter == "_" or caracter == "-":
                guiones += 1
            elif caracter in acentos:
                valido = False
            indice += 1
        if not mayusculas > 0 and not minusculas > 0 and not numeros > 0 and not guiones > 0:
            valido = False
    else:
        valido = False
    
    return valido
    


def guardar_registro(nombre, contraseña):

    pass