import customtkinter
from cargarConfig import loadConfiguration
from tkinter import *

textFont, fontSize, darkMode = loadConfiguration()

customtkinter.set_appearance_mode(darkMode)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Page:
    def __init__(self, master):
        self.master = master
        self.frame = customtkinter.CTkFrame(master, width=400, corner_radius=0)
        # self.frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=1, anchor="c")
        

    def show(self):
        self.frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)

    def hide(self):
        self.frame.grid_forget()

class AyudaPage(Page):
    def __init__(self, master):
        super().__init__(master)
        self.text = customtkinter.CTkLabel(self.frame, text="Ventana de ayuda!", font=(textFont, fontSize + 12))
        self.text.pack(pady=30)
        volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(textFont, fontSize), command=self.volver, fg_color='dark red')
        volver_button.pack(pady=30)

    def volver(self):
        self.hide()
        self.master.show_main_page()

