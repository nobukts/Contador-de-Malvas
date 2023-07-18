from tkinter import *
from tkinter import ttk

def preferencias():
    ventanaPreferencias = Tk()
    
    titulo = Label(ventanaPreferencias, text="Preferencias")
    titulo.config(font=("Verdana",36))
    titulo.grid(padx=10,pady=10,row=0,column=0)
    
    modoOscuro = Label(ventanaPreferencias, text="Modo Oscuro")
    modoOscuro.config(font=("Verdana",24))
    modoOscuro.grid(padx=10,pady=10,row=1, column=0)
    
    switchMode = Button(ventanaPreferencias,text="Apagado", width=10)
    switchMode.grid(padx=10,pady=10,row=1, column=1)
    
    fuente = Label(ventanaPreferencias, text="Tipografía")
    fuente.config(font=("Verdana",24))
    fuente.grid(padx=10,pady=10,row=2, column=0)
    
    listaFuentes = ttk.Combobox(ventanaPreferencias,state="readonly", values=["Verdana", "Monospace", "Consolas"])
    listaFuentes.grid(padx=10,pady=10,row=2, column=1)
    
    tamaño = Label(ventanaPreferencias, text="Tamaño de letra")
    tamaño.config(font=("Verdana",24))
    tamaño.grid(padx=10,pady=10,row=3, column=0)
    
    listaTamaño = ttk.Combobox(ventanaPreferencias,state="readonly", values=["Pequeño", "Mediano", "Grande"])
    listaTamaño.grid(padx=10,pady=10,row=3, column=1)
    ventanaPreferencias.mainloop()