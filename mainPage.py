from tkinter import *
import customtkinter
from page import Page
from cargarConfig import loadConfiguration

textFont, fontSize, darkMode = loadConfiguration()

customtkinter.set_appearance_mode(darkMode)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MainPage(Page):
    def __init__(self, master):
        super().__init__(master)
        self.frame.grid_rowconfigure((0,1,2,3), weight=1)
        self.frame.grid_columnconfigure((0,1,2), weight=1)

        # Title at the top, centered and aligned
        self.text = customtkinter.CTkLabel(self.frame, text="Contador de malvas", font=(textFont, fontSize + 12),width=50)
        self.text.grid(row=0, column=1, columnspan=1, pady=30,padx=30, sticky="n")  # Use sticky="n" for top alignment

        # Buttons centered vertically and horizontally, aligned to center
        self.cell1 = customtkinter.CTkButton(self.frame, text="Abrir archivo", width=10, command=self.master.show_abrir_archivo_page, font=(textFont, fontSize))
        self.cell1.grid(row=1, column=1, pady=30,padx=30, sticky="nsew")  # Use sticky="nsew" for center alignment

        self.cell2 = customtkinter.CTkButton(self.frame, text="Preferencias", width=10, font=(textFont, fontSize), command=self.master.show_preferencias_page)
        self.cell2.grid(row=2, column=1, pady=30,padx=30, sticky="nsew")  # Use sticky="nsew" for center alignment

        self.cell3 = customtkinter.CTkButton(self.frame, text="Ayuda", width=10, font=(textFont, fontSize), command=self.mostrar_ayuda)
        self.cell3.grid(row=3, column=1, pady=30,padx=30, sticky="nsew")  # Use sticky="nsew" for center alignment

    def mostrar_ayuda(self):
        self.hide()
        self.master.show_ayuda_page()