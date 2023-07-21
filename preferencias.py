from tkinter import *
from tkinter import ttk

def preferencias():

    def Darkmode(event):
        f = open("config.txt","r")
        contentFile = f.readline() + f.readline()
        f.close()

        f = open("config.txt","w")
        if switchMode.get() == 'Claro':
            f.write(contentFile + "darkMode = 0")
            colorBg = '#ffffff'
            colorFg = '#000000'
        else:
            f.write(contentFile + "darkMode = 1")
            colorBg = '#26242f'
            colorFg = '#ffffff'
        
        ventanaPreferencias.config(bg=colorBg)
        titulo.config(bg=colorBg,fg=colorFg)
        fuente.config(bg=colorBg,fg=colorFg)
        tamaño.config(bg=colorBg,fg=colorFg)
        modoOscuro.config(bg=colorBg,fg=colorFg)
        f.close()

    def FontType(event):
        f = open("config.txt","r")
        contentFile = f.readlines()[1:3]
        fontSize = contentFile[0][13:15]
        f.close()

        f = open("config.txt","w")
        if listaFuentes.get() == "Verdana":
            f.write("letterType = \"Verdana\"\n" + contentFile[0] + contentFile[1])
            textFont = "Verdana"
        if listaFuentes.get() == "Monospace":
            f.write("letterType = \"Monospace\"\n" + contentFile[0] + contentFile[1])
            textFont = "Monospace"
        if listaFuentes.get() == "Consolas":
            f.write("letterType = \"Consolas\"\n" + contentFile[0] + contentFile[1])
            textFont = "Consolas"
        
        titulo.config(font=(textFont,int(fontSize)+12))
        fuente.config(font=(textFont,int(fontSize)))
        tamaño.config(font=(textFont,int(fontSize)))
        modoOscuro.config(font=(textFont,int(fontSize)))
        f.close()
    
    def FontSize(event):
        f = open("config.txt","r")
        contentFile = f.readline()
        f.readline()
        contentFile2 = f.readline()
        textFont = contentFile.split("\"")[1]
        f.close()

        f = open("config.txt","w")
        if listaTamaño.get() == "Pequeño":
            f.write(contentFile + "letterSize = 12\n" + contentFile2)
            fontSize = 12
        if listaTamaño.get() == "Mediano":
            f.write(contentFile + "letterSize = 24\n" + contentFile2)
            fontSize = 24
        if listaTamaño.get() == "Grande":
            f.write(contentFile + "letterSize = 36\n" + contentFile2)
            fontSize = 36
        
        titulo.config(font=(textFont,int(fontSize)+12))
        fuente.config(font=(textFont,int(fontSize)))
        tamaño.config(font=(textFont,int(fontSize)))
        modoOscuro.config(font=(textFont,int(fontSize)))
        f.close()
    
    #load config file
    def loadConfiguration():
        #Declarate globals variables
        global textFont
        global fontSize
        global colorBg
        global colorFg
        global preConfgFont
        global preConfgSize
        global preConfgDark
        #load config file
        f = open("config.txt","r")
        preConfgFontConditional = f.readline().split("\"")[1]
        if preConfgFontConditional == "Verdana":
            preConfgFont = 0
            textFont = "Verdana"
        if preConfgFontConditional == "Monospace":
            preConfgFont = 1
            textFont = "Monospace"
        if preConfgFontConditional == "Consolas":
            preConfgFont = 2
            textFont = "Consolas"
        preConfgSizeConditional = f.readline()[13:15]
        if preConfgSizeConditional == "12":
            preConfgSize = 0
            fontSize = 12
        if preConfgSizeConditional == "24":
            preConfgSize = 1
            fontSize = 24
        if preConfgSizeConditional == "36":
            preConfgSize = 2
            fontSize = 36
        preConfgDark = f.readline()
        f.close()
        if preConfgDark[11] == '1':
            colorBg = '#26242f'
            colorFg = '#ffffff'
        else:
            colorBg = '#ffffff'
            colorFg = '#000000'
    
    loadConfiguration()
    ventanaPreferencias = Tk()
    ventanaPreferencias.config(bg=colorBg)
    ventanaPreferencias.minsize(600,350)

    #widgets
    titulo = Label(ventanaPreferencias, text="Preferencias",bg=colorBg, fg=colorFg)
    titulo.config(font=(textFont,fontSize+12))

    fuente = Label(ventanaPreferencias, text="Tipografía",bg=colorBg, fg=colorFg)
    fuente.config(font=(textFont,fontSize))
    
    listaFuentes = ttk.Combobox(ventanaPreferencias,state="readonly", values=["Verdana", "Monospace", "Consolas"])
    listaFuentes.current(preConfgFont)
    listaFuentes.bind('<<ComboboxSelected>>',FontType)

    tamaño = Label(ventanaPreferencias, text="Tamaño de letra",bg=colorBg, fg=colorFg)
    tamaño.config(font=(textFont,fontSize))
    
    listaTamaño = ttk.Combobox(ventanaPreferencias,state="readonly", values=["Pequeño", "Mediano", "Grande"])
    listaTamaño.current(preConfgSize)
    listaTamaño.bind('<<ComboboxSelected>>',FontSize)
    
    modoOscuro = Label(ventanaPreferencias, text="Modo Oscuro",bg=colorBg, fg=colorFg)
    modoOscuro.config(font=(textFont,fontSize))
    
    switchMode = ttk.Combobox(ventanaPreferencias,state="readonly", values=["Claro", "Oscuro"])
    switchMode.current(preConfgDark[11])
    switchMode.bind('<<ComboboxSelected>>',Darkmode)

    #grid
    ventanaPreferencias.rowconfigure(0,weight=1)
    ventanaPreferencias.rowconfigure(1,weight=1)
    ventanaPreferencias.rowconfigure(2,weight=1)
    ventanaPreferencias.rowconfigure(3,weight=1)
    ventanaPreferencias.columnconfigure(0,weight=1)
    ventanaPreferencias.columnconfigure(1,weight=1)

    titulo.grid(row=0,column=0,columnspan=1, sticky=N)
    fuente.grid(row = 1, column=0, sticky=W)
    listaFuentes.grid(row = 1, column=1, sticky=W)
    tamaño.grid(row = 2, column=0, sticky=W)
    listaTamaño.grid(row = 2, column=1, sticky=W)
    modoOscuro.grid(row = 3, column=0, sticky=W)
    switchMode.grid(row = 3, column=1, sticky=W)

    
    ventanaPreferencias.mainloop()