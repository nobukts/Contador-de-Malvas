from tkinter import *
import customtkinter
from page import Page
# from cargarConfig import loadConfiguration
from settings import app_settings

class PreferenciasPage(Page):
    def __init__(self, master, previous_page,abrir_archivo,analisis_foto,analisis_video,analisis_transmision):
        super().__init__(master)
        self.previous_page = previous_page
        self.abrir_archivo = abrir_archivo
        self.analisis_foto = analisis_foto
        self.analisis_video = analisis_video
        self.analisis_transmision = analisis_transmision

        #Load configuration
        app_settings.load_configuration()
        textFont = app_settings.textFont
        fontSize = app_settings.fontSize
        darkMode = app_settings.darkMode

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
        self.switch_var = customtkinter.StringVar(value="dark" if darkMode else "light")
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

        mode_string = "dark" if self.switch_var.get() == "dark" else "light"
        customtkinter.set_appearance_mode(mode_string)
        
        if self.switch_var.get() == "light":
            app_settings.update_dark_mode(False)
        else:
            app_settings.update_dark_mode(True)
        
        app_settings.save_configuration()

    def saveFontType(self, choice):

        if self.listaFuentes.get() == "Verdana":
            app_settings.update_font("Verdana")
        elif self.listaFuentes.get() == "Monospace":
            app_settings.update_font("Monospace")
        elif self.listaFuentes.get() == "Consolas":
            app_settings.update_font("Consolas")

        app_settings.save_configuration()
        self.update_widgets_font_and_size()

        self.previous_page.update_widgets_font_and_size()
        self.abrir_archivo.update_widgets_font_and_size()
        self.analisis_foto.update_widgets_font_and_size()
        self.analisis_video.update_widgets_font_and_size()
        self.analisis_transmision.update_widgets_font_and_size()

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

        app_settings.update_font_size(fontSize)
        app_settings.save_configuration()
        self.update_widgets_font_and_size()

        self.previous_page.update_widgets_font_and_size()
        self.abrir_archivo.update_widgets_font_and_size()
        self.analisis_foto.update_widgets_font_and_size()
        self.analisis_video.update_widgets_font_and_size()
        self.analisis_transmision.update_widgets_font_and_size()

        f.close()

    def update_widgets_font_and_size(self):
        # Actualizar la fuente y el tamaño de todos los widgets en la página
        self.titulo.configure(font=(app_settings.textFont, int(app_settings.fontSize)+12))
        self.fuente.configure(font=(app_settings.textFont, int(app_settings.fontSize)))
        self.tamaño.configure(font=(app_settings.textFont, int(app_settings.fontSize)))
        self.modoOscuro.configure(font=(app_settings.textFont, int(app_settings.fontSize)))
        self.volver_button.configure(font=(app_settings.textFont, int(app_settings.fontSize)))

    def show(self):
        self.frame.grid(row=1, column=1, sticky="nswe")

    def hide(self):
        self.frame.grid_forget()
