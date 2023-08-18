from tkinter import *
from abrirArchivo import AbrirArchivo
from preferencias import Prefference
import customtkinter
from cargarConfig import loadConfiguration

#Load configuration
textFont, fontSize, darkMode = loadConfiguration()

customtkinter.set_appearance_mode(darkMode)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Ayuda(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # configure window
        self.title("Inicio")
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
        self.text = customtkinter.CTkLabel(self.root, text="Ventana de ayuda!", font=(textFont,fontSize+12))
        self.text.pack()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Configure windows
        self.title("Inicio.py")
        self.geometry(f"{600}x{350}")
        self.minsize(600,350)
        
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.root = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.root.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.root.grid_rowconfigure(4, weight=1)

        #Pantalla de inicio
        self.text = customtkinter.CTkLabel(self.root, text="Contador de malvas", font=(textFont,fontSize+12))
        self.text.pack(pady=30)
        
        self.cell1 = customtkinter.CTkButton(self.root, text="Abrir archivo", width=10, command=self.open_toplevelAbrirArchivo, font=(textFont,fontSize))
        self.cell1.pack()

        self.cell2 = customtkinter.CTkButton(self.root, text="Preferencias", width=10, command=self.open_toplevelPreferencias, font=(textFont,fontSize))
        self.cell2.pack(pady=30)

        self.toplevel_window = None

        self.cell3 = customtkinter.CTkButton(self.root, text="Ayuda", width=10, font=(textFont,fontSize), command=self.open_toplevelAyuda)
        self.cell3.pack()
        
        self.mainloop()

    def cerrar_toplevel(self):
        self.toplevel_window.destroy()
        #Load configuration
        textFont, fontSize, darkMode = loadConfiguration()
        self.text.configure(font=(textFont,fontSize+12))
        self.cell1.configure(font=(textFont,fontSize))
        self.cell2.configure(font=(textFont,fontSize))
        self.cell3.configure(font=(textFont,fontSize))
        
    
    def open_toplevelPreferencias(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Prefference(self)
            self.toplevel_window.protocol("WM_DELETE_WINDOW", self.cerrar_toplevel)
        else:
            self.toplevel_window.focus()
    
    def open_toplevelAbrirArchivo(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AbrirArchivo(self)
        else:
            self.toplevel_window.focus()
    
    def open_toplevelAyuda(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Ayuda(self)
        else:
            self.toplevel_window.focus()
            
App()