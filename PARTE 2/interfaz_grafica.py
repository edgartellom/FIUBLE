from tkinter import *
from tkinter import messagebox
from registro import *

def ventana():
    

    ventana=Tk()
    ventana.title("Login")
    ventana.iconbitmap("cuantico.ico")
    ventana.resizable(0,0)
    ventana.geometry("300x150")

    frm1 = Frame()
    frm1.pack()
    frm1.config(bg="gray")
    frm1.config(width="300", height="150")
    
    
    textoEntrada = Label(frm1, text="Usuario:")
    textoEntrada.place(x=25, y=15)

    entrada = Entry(frm1)
    entrada.place(x=150, y=15)

    textoEntradaClave = Label(frm1, text="Clave:")
    textoEntradaClave.place(x=25, y=55)

    entradaClave = Entry(frm1)
    entradaClave.config(show="*")
    entradaClave.place(x=150, y=55)

    botonIngresar = Button(frm1, text="Ingresar", command=lambda: iniciar_sesion(entrada.get(), entradaClave.get()))
    botonIngresar.place(x=187, y=90)
    
    botonRegistro = Button(frm1, text="Registrar", command=lambda: nuevo_frame()) 
    botonRegistro.place(x=187, y=120)

    ventana.mainloop()
    

def nuevo_frame():

    ventana2=Tk()
    ventana2.title("Login")
    ventana2.iconbitmap("cuantico.ico")
    ventana2.resizable(0,0)
    ventana2.geometry("300x150")

    frm2 = Frame(ventana2)
    frm2.pack()
    frm2.config(bg="blue")
    frm2.config(width="300", height="150")
    
    
    textoEntrada = Label(frm2, text="Usuario:")
    textoEntrada.place(x=25, y=15)

    entrada = Entry(frm2)
    entrada.place(x=150, y=15)

    textoEntradaClave = Label(frm2, text="Clave:")
    textoEntradaClave.place(x=25, y=55)

    entradaClave = Entry(frm2)
    entradaClave.config(show="*")
    entradaClave.place(x=150, y=55)

ventana()