from tkinter import *
import customtkinter
from cargarConfig import loadConfiguration
from realizarAnalisisFoto import AnalisisFoto
from realizarAnalisisVideo import AnalisisVideo
from realizarAnalisisTransmision import AnalisisTransmision

class AbrirArchivo(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configure window
        self.title("Abrir archivo")
        self.geometry(f"{600}x{350}")
        self.minsize(600,350)
        self.maxsize(600,350)

        #Load configuration
        textFont, fontSize, darkMode = loadConfiguration()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.root = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.root.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.root.grid_rowconfigure(4, weight=1)
        
        #widgets
        self.text = customtkinter.CTkLabel(self.root, text="Elegir formato de análisis", font=(textFont,fontSize+12))
        self.text.pack(pady=30)

        self.cell1 = customtkinter.CTkButton(self.root, text="Imagen", width=10, font=(textFont,fontSize), command=AnalisisFoto)
        self.cell1.pack()

        self.cell1 = customtkinter.CTkButton(self.root, text="Video", width=10, font=(textFont,fontSize), command=AnalisisVideo)
        self.cell1.pack(pady=30)

        self.cell1 = customtkinter.CTkButton(self.root, text="En vivo", width=10, font=(textFont,fontSize), command=AnalisisTransmision)
        self.cell1.pack()