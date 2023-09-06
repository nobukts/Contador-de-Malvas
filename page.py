import customtkinter
from settings import app_settings
from tkinter import *

app_settings.load_configuration()

# Convierte el valor booleano a una cadena "dark" o "light"
mode_string = "dark" if app_settings.darkMode else "light"
# Establece el modo de apariencia
customtkinter.set_appearance_mode(mode_string)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Page:
    def __init__(self, master):
        self.master = master
        self.frame = customtkinter.CTkFrame(master, width=400, corner_radius=0)

    def update_widgets_font_and_size(self):
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize

    def show(self):
        self.update_widgets_font_and_size()
        self.frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)

    def hide(self):
        self.frame.grid_forget()

class AyudaPage(Page):
    def __init__(self, master):
        super().__init__(master)
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize
        self.text = customtkinter.CTkLabel(self.frame, text="Ventana de ayuda!", font=(self.textFont, self.fontSize + 12))
        self.text.pack(pady=30)
        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(self.textFont, self.fontSize), command=self.volver, fg_color='dark red')
        self.volver_button.pack(pady=30)

    def volver(self):
        self.hide()
        self.master.show_main_page()

    def update_widgets_font_and_size(self):
        super().update_widgets_font_and_size()  # Llama al método en la clase base
        textFont = app_settings.textFont
        fontSize = app_settings.fontSize
        self.text.configure(font=(textFont, fontSize + 12))
        self.volver_button.configure(font=(self.textFont, self.fontSize))

