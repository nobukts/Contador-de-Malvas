from tkinter import *
import customtkinter
from cargarConfig import loadConfiguration

class Prefference(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configure window
        self.title("Configuracion de preferencias")
        self.geometry(f"{600}x{350}")
        self.minsize(600,350)
        self.maxsize(600,350)

        #Load configuration
        textFont, fontSize, darkMode = loadConfiguration()
        if fontSize == 12:
            fontSizeString = "Pequeño"
        if fontSize == 24:
            fontSizeString = "Mediano"
        if fontSize == 36:
            fontSizeString = "Grande"

        #grid
        self.grid_rowconfigure((0,1,2),weight=1)
        self.grid_columnconfigure((0,1,2),weight=1)

        #grid root
        self.root = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.root.grid(row=1, column=1, sticky="nsew")
        self.root.grid_rowconfigure((0,1,2,3), weight=1)
        self.root.grid_columnconfigure((0,1), weight=1)
        
        #widgets
        self.titulo = customtkinter.CTkLabel(self.root, text="Preferencias", font=(textFont,fontSize+12))

        valorPrevio = customtkinter.StringVar(value=textFont)
        self.fuente = customtkinter.CTkLabel(self.root, text="Tipografía", font=(textFont,fontSize))
        self.listaFuentes = customtkinter.CTkComboBox(self.root,state="readonly", values=["Verdana", "Monospace", "Consolas"], command=self.saveFontType, variable=valorPrevio)

        valorPrevio = customtkinter.StringVar(value=fontSizeString)
        self.tamaño = customtkinter.CTkLabel(self.root, text="Tamaño de letra", font=(textFont,fontSize))
        self.listaTamaño = customtkinter.CTkComboBox(self.root,state="readonly", values=["Pequeño", "Mediano", "Grande"], command=self.saveFontSize, variable=valorPrevio)
        
        self.modoOscuro = customtkinter.CTkLabel(self.root, text="Modo Oscuro", font=(textFont,fontSize))
        self.switch_var = customtkinter.StringVar(value=darkMode)
        self.switchMode = customtkinter.CTkSwitch(self.root,text="", command=self.switch_event, variable=self.switch_var, onvalue="dark", offvalue="light")

        
        self.titulo.grid(row = 0, column = 0, columnspan = 2)
        self.fuente.grid(row = 1, column = 0)
        self.listaFuentes.grid(row = 1, column = 1)
        self.tamaño.grid(row = 2, column = 0)
        self.listaTamaño.grid(row = 2, column = 1)
        self.modoOscuro.grid(row = 3, column = 0)
        self.switchMode.grid(row = 3, column = 1)
    
    def switch_event(self):
        f = open("config.txt","r")
        contentFile = f.readline() + f.readline()
        f.close()

        f = open("config.txt","w")
        if self.switch_var.get() == "light":
            customtkinter.set_appearance_mode("light")
            f.write(contentFile + "darkMode = 0")
        else:
            customtkinter.set_appearance_mode("dark")
            f.write(contentFile + "darkMode = 1")
        f.close()
    
    def saveFontType(self, choice):
        f = open("config.txt","r")
        contentFile = f.readlines()[1:3]
        fontSize = contentFile[0][13:15]
        f.close()

        f = open("config.txt","w")
        if self.listaFuentes.get() == "Verdana":
            f.write("letterType = \"Verdana\"\n" + contentFile[0] + contentFile[1])
            textFont = "Verdana"
        if self.listaFuentes.get() == "Monospace":
            f.write("letterType = \"Monospace\"\n" + contentFile[0] + contentFile[1])
            textFont = "Monospace"
        if self.listaFuentes.get() == "Consolas":
            f.write("letterType = \"Consolas\"\n" + contentFile[0] + contentFile[1])
            textFont = "Consolas"
        
        self.titulo.configure(font=(textFont,int(fontSize)+12))
        self.fuente.configure(font=(textFont,int(fontSize)))
        self.tamaño.configure(font=(textFont,int(fontSize)))
        self.modoOscuro.configure(font=(textFont,int(fontSize)))
        f.close()

    def saveFontSize(self, choice):
        f = open("config.txt","r")
        contentFile = f.readline()
        f.readline()
        contentFile2 = f.readline()
        textFont = contentFile.split("\"")[1]
        f.close()

        f = open("config.txt","w")
        if self.listaTamaño.get() == "Pequeño":
            f.write(contentFile + "letterSize = 12\n" + contentFile2)
            fontSize = 12
        if self.listaTamaño.get() == "Mediano":
            f.write(contentFile + "letterSize = 24\n" + contentFile2)
            fontSize = 24
        if self.listaTamaño.get() == "Grande":
            f.write(contentFile + "letterSize = 36\n" + contentFile2)
            fontSize = 36
        
        self.titulo.configure(font=(textFont,int(fontSize)+12))
        self.fuente.configure(font=(textFont,int(fontSize)))
        self.tamaño.configure(font=(textFont,int(fontSize)))
        self.modoOscuro.configure(font=(textFont,int(fontSize)))
        f.close()