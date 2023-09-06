from tkinter import *
import customtkinter
from page import Page
from settings import app_settings

app_settings.load_configuration()

# Convierte el valor booleano a una cadena "dark" o "light"
mode_string = "dark" if app_settings.darkMode else "light"
# Establece el modo de apariencia
customtkinter.set_appearance_mode(mode_string)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MainPage(Page):
    def __init__(self, master):
        super().__init__(master)
        
        self.frame.grid_rowconfigure((0,1,2,3), weight=1)
        self.frame.grid_columnconfigure((0,1,2), weight=1)
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize
        # self.update_widgets_font_and_size()  # Llama a esta función para configurar la tipografía y el tamaño de letra

        # Title at the top, centered and aligned
        self.text = customtkinter.CTkLabel(self.frame, text="Contador de malvas", font=(self.textFont, self.fontSize + 12), width=50)
        self.text.grid(row=0, column=1, columnspan=1, pady=30, padx=30, sticky="n")  # Use sticky="n" for top alignment

        # Buttons centered vertically and horizontally, aligned to center
        self.cell1 = customtkinter.CTkButton(self.frame, text="Abrir archivo", width=10, command=self.master.show_abrir_archivo_page, font=(self.textFont, self.fontSize))
        self.cell1.grid(row=1, column=1, pady=30, padx=30, sticky="nsew")  # Use sticky="nsew" for center alignment

        self.cell2 = customtkinter.CTkButton(self.frame, text="Preferencias", width=10, font=(self.textFont, self.fontSize), command=self.master.show_preferencias_page)
        self.cell2.grid(row=2, column=1, pady=30, padx=30, sticky="nsew")  # Use sticky="nsew" for center alignment

        self.cell3 = customtkinter.CTkButton(self.frame, text="Ayuda", width=10, font=(self.textFont, self.fontSize), command=self.mostrar_ayuda)
        self.cell3.grid(row=3, column=1, pady=30, padx=30, sticky="nsew")  # Use sticky="nsew" for center alignment

        self.exit_button = customtkinter.CTkButton(self.frame, text="Salir", width=10, font=(self.textFont, self.fontSize), fg_color='dark red', command=self.master.destroy)
        self.exit_button.grid(row=4, column=1, pady=30, padx=30, sticky="nsew")

    def mostrar_ayuda(self):
        self.hide()
        self.master.show_ayuda_page()

    def update_widgets_font_and_size(self):
        # Actualizar la fuente y el tamaño de letra de los widgets en la página principal
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize

        self.text.configure(font=(self.textFont, self.fontSize + 12))
        self.cell1.configure(font=(self.textFont, self.fontSize))
        self.cell2.configure(font=(self.textFont, self.fontSize))
        self.cell3.configure(font=(self.textFont, self.fontSize))
        self.exit_button.configure(font=(self.textFont, self.fontSize))