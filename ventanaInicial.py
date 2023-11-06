from tkinter import *
from page import Page, AyudaPage
from mainPage import MainPage
from abrirArchivoPage import AbrirArchivoPage
from preferencias_page import PreferenciasPage
from realizarAnalisisFoto import AnalisisFotoPage 
from realizarAnalisisVideo import AnalisisVideoPage
from realizarAnalisisTransmision import AnalisisTransmisionPage
import customtkinter
from settings import app_settings
from tkinter import messagebox

# Convierte el valor booleano a una cadena "dark" o "light"
mode_string = "dark" if app_settings.darkMode else "light"
# Establece el modo de apariencia
customtkinter.set_appearance_mode(mode_string)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Contador_de_Malvas.py")
        self.geometry(f"{1090}x{900}")
        self.minsize(1090, 900)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.main_page = MainPage(self)
        self.ayuda_page = AyudaPage(self)
        self.abrir_archivo_page = AbrirArchivoPage(self,self.main_page)
        self.analisis_foto = AnalisisFotoPage(self)
        self.analisis_video = AnalisisVideoPage(self)
        self.analisis_transmision = AnalisisTransmisionPage(self)
        self.preferencias_page = PreferenciasPage(self, self.main_page,self.abrir_archivo_page,self.analisis_foto,self.analisis_video,self.analisis_transmision)
        
        self.pages = {
            "main": self.main_page,
            "ayuda": self.ayuda_page,
            "abrir_archivo": AbrirArchivoPage(self, self.main_page),
            "preferencias": PreferenciasPage(self, self.main_page,self.abrir_archivo_page,self.analisis_foto,self.analisis_video,self.analisis_transmision),
            "analisis_foto": AnalisisFotoPage(self),
            "analisis_video": AnalisisVideoPage(self),
            "analisis_transmision": AnalisisTransmisionPage(self),
        }

        self.show_page("main")
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
    
    def on_closing(self):
        if messagebox.askokcancel("Cerrar", "¿Quieres cerrar la aplicación? Si no ha exportado sus datos, estos se perderán"):
            self.destroy()

    def show_page(self, page_name):
        for page in self.pages.values():
            page.hide()
        self.pages[page_name].show()

    def show_main_page(self):
        self.show_page("main")

    def show_ayuda_page(self):
        self.show_page("ayuda")

    def show_abrir_archivo_page(self):
        self.show_page("abrir_archivo")

    def show_preferencias_page(self):
        self.show_page("preferencias")

    def show_analisis_foto_page(self):
        self.show_page("analisis_foto")

    def show_analisis_video_page(self):
        self.show_page("analisis_video")

    def show_analisis_transmision_page(self):
        self.show_page("analisis_transmision")

if __name__ == "__main__":
    app = App()
    app.mainloop()