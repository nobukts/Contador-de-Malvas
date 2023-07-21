from tkinter import *
from realizarAnalisisFoto import iniciarAnalisis1
from realizarAnalisisVideo import iniciarAnalisis2
from realizarAnalisisTransmision import iniciarAnalisis3

def loadConfiguration():
    #Declarate globals variables
    global textFont
    global fontSize
    global colorBg
    global colorFg
    #load config file
    f = open("config.txt","r")
    preConfgFontConditional = f.readline().split("\"")[1]
    if preConfgFontConditional == "Verdana":
        textFont = "Verdana"
    if preConfgFontConditional == "Monospace":
        textFont = "Monospace"
    if preConfgFontConditional == "Consolas":
        textFont = "Consolas"
    preConfgSizeConditional = f.readline()[13:15]
    if preConfgSizeConditional == "12":
        fontSize = 12
    if preConfgSizeConditional == "24":
        fontSize = 24
    if preConfgSizeConditional == "36":
        fontSize = 36
    preConfgDark = f.readline()
    f.close()
    if preConfgDark[11] == '1':
        colorBg = '#26242f'
        colorFg = '#ffffff'
    else:
        colorBg = '#ffffff'
        colorFg = '#000000'

def abrirArchivo():
    #load config file
    loadConfiguration()
    
    nuevaVentana = Tk()
    nuevaVentana.config(bg=colorBg)
    nuevaVentana.minsize(620,350)
    
    text = Label(nuevaVentana,text="Elegir formato de análisis", bg=colorBg,fg=colorFg)
    text.pack()
    text.config(font=(textFont,fontSize+12))
    
    cell1 = Button(nuevaVentana, text="Imagen", width=10, command=iniciarAnalisis1, bg=colorBg,fg=colorFg)
    cell1.config(font=(textFont,fontSize))
    cell1.pack()
    
    cell2 = Button(nuevaVentana,text="Vídeo", width=10, command=iniciarAnalisis2, bg=colorBg,fg=colorFg)
    cell2.config(font=(textFont,fontSize))
    cell2.pack(pady=30)

    cell3 = Button(nuevaVentana,text="En vivo", width=10, command=iniciarAnalisis3, bg=colorBg,fg=colorFg)
    cell3.config(font=(textFont,fontSize))
    cell3.pack()
    
    nuevaVentana.mainloop()