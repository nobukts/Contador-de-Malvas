from tkinter import *
import customtkinter
from page import Page
from cargarConfig import loadConfiguration

class PreferenciasPage(Page):
    def __init__(self, master, previous_page):
        super().__init__(master)
        self.previous_page = previous_page
        

        #Load configuration
        textFont, fontSize, darkMode = loadConfiguration()
        if fontSize == 12:
            fontSizeString = "Pequeño"
        elif fontSize == 24:
            fontSizeString = "Mediano"
        elif fontSize == 36:
            fontSizeString = "Grande"

        self.frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        self.frame.grid_columnconfigure((0,1), weight=1)

        # Widgets
        self.titulo = customtkinter.CTkLabel(self.frame, text="Preferencias", font=(textFont,fontSize+12))

        valorPrevio = customtkinter.StringVar(value=textFont)
        self.fuente = customtkinter.CTkLabel(self.frame, text="Tipografía", font=(textFont,fontSize))
        self.listaFuentes = customtkinter.CTkComboBox(self.frame,state="readonly", values=["Verdana", "Monospace", "Consolas"], command=self.saveFontType, variable=valorPrevio)

        valorPrevio = customtkinter.StringVar(value=fontSizeString)
        self.tamaño = customtkinter.CTkLabel(self.frame, text="Tamaño de letra", font=(textFont,fontSize))
        self.listaTamaño = customtkinter.CTkComboBox(self.frame,state="readonly", values=["Pequeño", "Mediano", "Grande"], command=self.saveFontSize, variable=valorPrevio)
        
        self.modoOscuro = customtkinter.CTkLabel(self.frame, text="Modo Oscuro", font=(textFont,fontSize))
        self.switch_var = customtkinter.StringVar(value=darkMode)
        self.switchMode = customtkinter.CTkSwitch(self.frame,text="", command=self.switch_event, variable=self.switch_var, onvalue="dark", offvalue="light")

        
        self.titulo.grid(row = 0, column = 0, columnspan = 2, padx=20, pady=20)
        self.fuente.grid(row = 1, column = 0, padx=20, pady=20)
        self.listaFuentes.grid(row = 1, column = 1, padx=20, pady=20)
        self.tamaño.grid(row = 2, column = 0, padx=20, pady=20)
        self.listaTamaño.grid(row = 2, column = 1, padx=20, pady=20)
        self.modoOscuro.grid(row = 3, column = 0, padx=20, pady=20)
        self.switchMode.grid(row = 3, column = 1, padx=20, pady=20)

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", command=self.volver, font=(textFont, fontSize), fg_color='dark red')
        self.volver_button.grid(row=4, column=0, padx=20, pady=20)

    def volver(self):
        self.hide()  
        self.previous_page.show()

    def switch_event(self):
        f = open("config.txt", "r")
        contentFile = f.readline() + f.readline()
        f.close()

        f = open("config.txt", "w")
        if self.switch_var.get() == "light":
            customtkinter.set_appearance_mode("light")
            f.write(contentFile + "darkMode = 0")
        else:
            customtkinter.set_appearance_mode("dark")
            f.write(contentFile + "darkMode = 1")
        f.close()

    def saveFontType(self, choice):
        f = open("config.txt", "r")
        contentFile = f.readlines()[1:3]
        fontSize = contentFile[0][13:15]
        f.close()

        f = open("config.txt", "w")
        if self.listaFuentes.get() == "Verdana":
            f.write("letterType = \"Verdana\"\n" + contentFile[0] + contentFile[1])
            textFont = "Verdana"
        elif self.listaFuentes.get() == "Monospace":
            f.write("letterType = \"Monospace\"\n" + contentFile[0] + contentFile[1])
            textFont = "Monospace"
        elif self.listaFuentes.get() == "Consolas":
            f.write("letterType = \"Consolas\"\n" + contentFile[0] + contentFile[1])
            textFont = "Consolas"

        self.fuente.configure(font=(textFont, int(fontSize)))
        self.tamaño.configure(font=(textFont, int(fontSize)))
        self.modoOscuro.configure(font=(textFont, int(fontSize)))
        
        f.close()

    def saveFontSize(self, choice):
        f = open("config.txt", "r")
        contentFile = f.readline()
        f.readline()
        contentFile2 = f.readline()
        textFont = contentFile.split("\"")[1]
        f.close()

        f = open("config.txt", "w")
        if self.listaTamaño.get() == "Pequeño":
            f.write(contentFile + "letterSize = 12\n" + contentFile2)
            fontSize = 12
        elif self.listaTamaño.get() == "Mediano":
            f.write(contentFile + "letterSize = 24\n" + contentFile2)
            fontSize = 24
        elif self.listaTamaño.get() == "Grande":
            f.write(contentFile + "letterSize = 36\n" + contentFile2)
            fontSize = 36

        self.titulo.configure(font=(textFont, int(fontSize+12)))
        self.fuente.configure(font=(textFont, int(fontSize)))
        self.tamaño.configure(font=(textFont, int(fontSize)))
        self.modoOscuro.configure(font=(textFont, int(fontSize)))
        f.close()

    def show(self):
        self.frame.grid(row=1, column=1, sticky="nswe")

    def hide(self):
        self.frame.grid_forget()
