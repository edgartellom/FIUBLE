from tkinter import *
from tkinter import messagebox
from registro import *

def ventana():
    
    ventana=Tk()
    ventana.title("Login")
    ventana.iconbitmap("cuantico.ico")
    ventana.resizable(0,0)
    ventana.geometry("300x200")

    frm1 = Frame()
    frm1.pack()
    frm1.config(bg="gray")
    frm1.config(width="300", height="200")
    
    
    textoEntradaUsuario = Label(frm1, text="Usuario:")
    textoEntradaUsuario.place(x=25, y=15)

    entradaUsuario = Entry(frm1)
    entradaUsuario.place(x=150, y=15)

    textoEntradaClave = Label(frm1, text="Clave:")
    textoEntradaClave.place(x=25, y=55)

    entradaClave = Entry(frm1)
    entradaClave.config(show="*")
    entradaClave.place(x=150, y=55)

    botonIngresar = Button(frm1, text="Ingresar", command=lambda: iniciar_sesion(entradaUsuario.get(), entradaClave.get()))
    botonIngresar.place(x=187, y=90)
    
    botonRegistro = Button(frm1, text="Registrar", command=lambda: nuevo_frame()) 
    botonRegistro.place(x=187, y=120)

    ventana.mainloop()
    

def nuevo_frame():

    ventana2=Tk()
    ventana2.title("Login")
    ventana2.iconbitmap("cuantico.ico")
    ventana2.resizable(0,0)
    ventana2.geometry("300x200")

    frm2 = Frame(ventana2)
    frm2.pack()
    frm2.config(bg="blue")
    frm2.config(width="300", height="200")
    
    
    textoEntradaUsuario = Label(frm2, text="Usuario:")
    textoEntradaUsuario.place(x=25, y=15)

    entradaUsuario = Entry(frm2)
    entradaUsuario.place(x=150, y=15)

    textoEntradaClave1 = Label(frm2, text="Nueva Clave:")
    textoEntradaClave1.place(x=25, y=55)

    textoEntradaClave2 = Label(frm2, text="Reingrese Clave:")
    textoEntradaClave2.place(x=25, y=90)

    entradaClave1 = Entry(frm2)
    entradaClave1.config(show="*")
    entradaClave1.place(x=150, y=55)

    entradaClave2 = Entry(frm2)
    entradaClave2.config(show="*")
    entradaClave2.place(x=150, y=90)

    botonRegistro = Button(frm2, text="Registrar", command=lambda: guardar_registro(entradaUsuario.get(), entradaClave1.get(), entradaClave2.get())) 
    botonRegistro.place(x=187, y=115)

    botonRegresar = Button(frm2, text="Regresar", command=ventana2.destroy).place(x=187, y=155)
 

ventana()