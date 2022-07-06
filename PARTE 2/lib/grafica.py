from tkinter import *
from tkinter import messagebox
from . import usuarios
import sys



ICONO = sys.path[0] + "/assets/cuantico.ico"






def solicitar_credenciales(indice_jugador):
    '''
        Abre una ventana con tkinter que le solicita al
        jugador un usuario y contraseña. Finalmente retorna
        esos datos en un listado

        ~ Tomas Fernández Moreno
    '''

    ventana=Tk()
    ventana.title("Login usuario" + str(indice_jugador))
    ventana.iconbitmap(ICONO)
    ventana.resizable(0,0)
    ventana.geometry("300x200")        

    credenciales = ["", ""]
    def definir_usuario(usuario, clave):
        '''
            Establece las credenciales introducidas por el
            usuario en la variable correspondiente para que
            sea accesible desde la función padre siempre y
            cuando esos datos sean válidos

            ~ Tomas Fernández Moreno
        '''

        # Evita que los datos vengan vacíos
        if usuario == "" or clave == "": 
            messagebox.showerror("Login", "Ingrese un Usuario y Clave!")

        # En caso de que el inicio de sesión sea correcto
        # establece la variable de credenciales con
        # los datos y cierra la ventana
        elif usuarios.iniciar_sesion(usuario, clave):
            messagebox.showinfo("Login", "Usuario y Clave Correctos!")
            credenciales[0] = usuario
            credenciales[1] = clave
            ventana.destroy()

        # Si el login fue erróneo lo notifica con una
        # ventana emergente y vacía los campos
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
    '''
        Abre una ventana con tkinter que le solicita al
        jugador un nombre de usuario y una contraseña que
        tendrá que repetir 2 veces. Una vez los datos
        fueron validados, llama a una función que escriba
        las credenciales en usuarios.csv

        ~ Tomas Fernández Moreno
    '''

    ventana=Tk()
    ventana.title("Registro")
    ventana.iconbitmap(ICONO)
    ventana.resizable(0,0)
    ventana.geometry("300x200")

    def procesar_credenciales(usuario, clave, clave_repetida):
        '''
            Hace todas las validaciones de nombre y contraseña.
            En caso de que sean correctas registra el usuario

            ~ Tomas Fernández Moreno
        '''
        
        if usuarios.nombre_valido(usuario):
            if clave == clave_repetida:
                if usuarios.clave_valida(clave):

                    # En caso de que todas las validaciones sean
                    # satisfactorias, registra el usuario y destruye
                    # la ventana
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
