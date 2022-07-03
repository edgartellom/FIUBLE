from tkinter import *
from tkinter import messagebox
from . import usuarios, archivos
import sys

ICONO = sys.path[0] + "/assets/cuantico.ico"

def solicitar_credenciales(indice_jugador):

    ventana=Tk()
    ventana.title("Login usuario" + str(indice_jugador))
    ventana.iconbitmap(ICONO)
    ventana.resizable(0,0)
    ventana.geometry("300x200")        

    credenciales = ["", ""]
    def definir_usuario(usuario, clave):
        credenciales[0] = usuario
        credenciales[1] = clave

        if usuario == "" or clave == "": 
            messagebox.showerror("Login", "Ingrese un Usuario y Clave!")
        elif usuarios.iniciar_sesion(credenciales[0], credenciales[1]):
            messagebox.showinfo("Login", "Usuario y Clave Correctos!")
            ventana.destroy()
        else:
            messagebox.showerror("Login", "Alguno de los datos ingresados es incorrecto!")
            entradaUsuario.delete(0, END)
            entradaUsuario.insert(0, "")
            entradaClave.delete(0, END)
            entradaClave.insert(0, "")
    
    textoEntradaUsuario = Label(ventana, text="Usuario:")
    textoEntradaUsuario.place(x=25, y=15)

    entradaUsuario = Entry(ventana)
    entradaUsuario.place(x=150, y=15)

    textoEntradaClave = Label(ventana, text="Clave:")
    textoEntradaClave.place(x=25, y=55)

    entradaClave = Entry(ventana)
    entradaClave.config(show="*")
    entradaClave.place(x=150, y=55)

    botonIngresar = Button(ventana, text="Ingresar", command=lambda: definir_usuario(entradaUsuario.get(), entradaClave.get()))
    botonIngresar.place(x=187, y=90)
    
    botonRegistro = Button(ventana, text="Registrar", command=lambda: solicitar_credenciales_nuevo_usuario()) 
    botonRegistro.place(x=187, y=120)

    ventana.mainloop()

    return credenciales
    

def solicitar_credenciales_nuevo_usuario():

    ventana=Tk()
    ventana.title("Registro")
    ventana.iconbitmap(ICONO)
    ventana.resizable(0,0)
    ventana.geometry("300x200")

    credenciales = ["", "", ""]
    def procesar_credenciales(usuario, clave, clave_repetida):
        credenciales[0] = usuario
        credenciales[1] = clave
        credenciales[2] = clave_repetida

        if usuarios.nombre_valido(usuario):
            if clave == clave_repetida:
                if usuarios.clave_valida(clave):
                    usuarios.registrar_usuario(usuario, clave)
                    messagebox.showinfo("Registro", "Usuario y Clave registrados con éxito!")
                    ventana.destroy()
                else:
                    messagebox.showerror("Registro", "Clave ingresada inválida! Debe ser entre 8 y 12 caracteres y contener al menos una minúscula, una mayúscula, un número y un guión ('-' o '_')")
            else:
                messagebox.showerror("Registro", "Claves ingresadas no coinciden!")
        else:
            messagebox.showerror("Registro", "Nombre ingresado inválido! Debe ser entre 4 y 15 caracteres entre letras, números y '_'")
    
    textoEntradaUsuario = Label(ventana, text="Usuario:")
    textoEntradaUsuario.place(x=25, y=15)

    textoEntradaClave1 = Label(ventana, text="Nueva Clave:")
    textoEntradaClave1.place(x=25, y=55)

    textoEntradaClave2 = Label(ventana, text="Reingrese Clave:")
    textoEntradaClave2.place(x=25, y=90)

    entradaUsuario = Entry(ventana)
    entradaUsuario.place(x=150, y=15)

    entradaClave1 = Entry(ventana)
    entradaClave1.config(show="*")
    entradaClave1.place(x=150, y=55)

    entradaClave2 = Entry(ventana)
    entradaClave2.config(show="*")
    entradaClave2.place(x=150, y=90)

    botonRegistro = Button(ventana, text="Registrar", command=lambda: procesar_credenciales(entradaUsuario.get(), entradaClave1.get(), entradaClave2.get())) 
    botonRegistro.place(x=187, y=115)

    botonRegresar = Button(ventana, text="Regresar", command=ventana.destroy).place(x=187, y=155)
 

# ventana()