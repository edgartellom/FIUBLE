from prueba_archivos import *
from tkinter import messagebox

def iniciar_sesion(usuario, clave):
	claves = procesar_archivo()
	if usuario in claves and clave == claves[usuario]:
		messagebox.showinfo("Login", "Usuario y Clave Correctos")
	else:
		messagebox.showerror("Login", "Alguno de los datos ingresados es incorrecto")




# REGISTRO = []
# def registrar_jugador(nombre):
