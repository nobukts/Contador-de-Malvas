from tkinter import *
from abrirArchivo import abrirArchivo
from preferencias import preferencias

def ayuda():
    nuevaVentana = Tk()
    nuevaVentana.config(bg=colorBg)
    nuevaVentana.minsize(600,350)

    text = Label(nuevaVentana,text="Ventana de ayuda!", bg=colorBg, fg=colorFg)    
    text.pack()
    text.config(font=(textFont,fontSize+12))
    nuevaVentana.mainloop()
    
def pantallaInicio():
    
    text = Label(root,text="Contador de malvas",bg=colorBg,fg=colorFg)
    text.pack()
    text.config(font=(textFont,fontSize+12))
    
    cell1 = Button(root, text="Abrir archivo", width=10, command=abrirArchivo, bg=colorBg,fg=colorFg)
    cell1.pack()
    cell1.config(font=(textFont,fontSize))

    cell2 = Button(root,text="Preferencias", width=10, command=preferencias, bg=colorBg,fg=colorFg)
    cell2.config(font=(textFont,fontSize))
    cell2.pack(pady=30)

    cell3 = Button(root,text="Ayuda", width=10, command=ayuda, bg=colorBg,fg=colorFg)
    cell3.config(font=(textFont,fontSize))
    cell3.pack()

#load config file
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

#widgets
loadConfiguration()
root = Tk()
root.config(bg=colorBg)
root.minsize(600,350)

pantallaInicio()        

root.mainloop()