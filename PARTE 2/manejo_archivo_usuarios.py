def leer_archivo(archivo):
    linea = archivo.readline()
    if linea:
        linea = linea.rstrip("\n")
    else:
        linea = ","

    return linea.split(",")


def procesar_archivo():
    with open("usuarios.csv", "r") as archivo:
        usuario, clave = leer_archivo(archivo)
        registro = {usuario:clave}
        
        while usuario:
            usuario, clave = leer_archivo(archivo)
            
            registro[usuario] = clave

    return registro

def guardar_nuevos_datos(nuevo_usuario, nueva_clave):
    with open ("usuarios.csv", "a") as archivo:
        linea = f"{nuevo_usuario},{nueva_clave}\n"
        archivo.write(linea)
    
    return

print (procesar_archivo())