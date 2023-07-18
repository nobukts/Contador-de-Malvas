from tkinter import *
from realizarAnalisisFoto import iniciarAnalisis1
from realizarAnalisisVideo import iniciarAnalisis2
from realizarAnalisisTransmision import iniciarAnalisis3

def abrirArchivo():
    nuevaVentana = Tk()
    
    text = Label(nuevaVentana,text="Elegir formato de análisis")
    text.pack(anchor=CENTER)
    text.config(font=("Verdana",36))
    text.grid(padx=10,pady=10,row=0,column=0)

    cell1 = Button(nuevaVentana, text="Imagen", width=10, command=iniciarAnalisis1)
    cell1.config(font=("Verdana",24))
    cell1.grid(padx=10,pady=10, row=1, column=0)

    cell2 = Button(nuevaVentana,text="Vídeo", width=10, command=iniciarAnalisis2)
    cell2.config(font=("Verdana",24))
    cell2.grid(padx=10,pady=10, row=2, column=0)

    cell3 = Button(nuevaVentana,text="En vivo", width=10, command=iniciarAnalisis3)
    cell3.config(font=("Verdana",24))
    cell3.grid(padx=10,pady=10, row=3, column=0)
    nuevaVentana.mainloop()