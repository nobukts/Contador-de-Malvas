from tkinter import *
from abrirArchivo import abrirArchivo
from preferencias import preferencias

def ayuda():
    nuevaVentana = Tk()
    text = Label(nuevaVentana,text="Hola!")    
    text.grid(row=0, column=0)
    text.config(font=("Verdana",36))
    nuevaVentana.mainloop()
    
def pantallaInicio():
    text = Label(root,text="Contador de malvas")
    text.pack(anchor=CENTER)
    text.config(font=("Verdana",36))
    text.grid(padx=10,pady=10,row=0,column=0)

    cell1 = Button(root, text="Abrir archivo", width=10, command=abrirArchivo)
    cell1.config(font=("Verdana",24))
    cell1.grid(padx=10,pady=10, row=1, column=0)

    cell2 = Button(root,text="Preferencias", width=10, command=preferencias)
    cell2.config(font=("Verdana",24))
    cell2.grid(padx=10,pady=10, row=2, column=0)

    cell3 = Button(root,text="Ayuda", width=10, command=ayuda)
    cell3.config(font=("Verdana",24))
    cell3.grid(padx=10,pady=10, row=3, column=0)

root = Tk()

pantallaInicio()        

root.mainloop()