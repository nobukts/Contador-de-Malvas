from tkinter import *
import customtkinter
from page import Page
from settings import app_settings
import cv2
from PIL import Image, ImageTk
import pandas as pd

class AnalisisTransmisionPage(Page):
    def __init__(self,master):
        super().__init__(master)
        
        app_settings.load_configuration()
        
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize
        
        # configure grid layout (4x4)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.root = customtkinter.CTkFrame(self.frame, width=140, corner_radius=0)
        self.root.grid(row=1, column=1, sticky="nsew")
        self.root.grid_columnconfigure((0,1),weight=1)
        self.root.grid_rowconfigure((0,1), weight=1)

        self.rootAnalisis = customtkinter.CTkFrame(self.root, width=140, corner_radius=0)
        self.rootAnalisis.grid(row=0, rowspan=2, column=1)
        self.rootAnalisis.grid_rowconfigure((0,1,2,3,4), weight=1)

        # Pantalla de inicio
        self.toggle_transmission_button = customtkinter.CTkButton(self.root, text="Iniciar Transmisión", width=25, command=self.toggle_transmission)
        self.toggle_transmission_button.grid(row=1, column=0)

        self.lblInputImage1 = customtkinter.CTkLabel(self.root, text="")
        self.lblInputImage1.grid(row=0, column=0)

        self.text = customtkinter.CTkLabel(self.rootAnalisis, text="Análisis", font=(self.textFont, self.fontSize+12))
        self.text.grid(column=0, pady=10)

        self.lblInfo3 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo3.grid(row=1, pady=15, padx=5)
        self.lblInfo4 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas volteadas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo4.grid(row=2, pady=5, padx=5)
        self.lblInfo5 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas por minuto: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo5.grid(row=3, pady=15, padx=5)
        self.lblInfo6 = customtkinter.CTkButton(self.rootAnalisis, text="Exportar excel", command=self.exportar_excel)
        self.lblInfo6.grid(row=4, pady=5)
        
        self.cap = None # Inicialmente, no hay captura activa

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(self.textFont, self.fontSize), command=self.volver, fg_color='dark red')
        self.volver_button.grid(row=3, column=1, pady=30)

        self.camera_list = self.get_camera_list()
        self.camera_var = StringVar(self.frame)
        if len(self.camera_list) > 0:
            self.camera_var.set(self.camera_list[0])  # Establece la primera cámara como predeterminada

        self.camera_dropdown = customtkinter.CTkOptionMenu(self.frame, variable=self.camera_var, values=self.camera_list)
        self.camera_dropdown.grid(row=2, column=1, pady=10)
        self.camera_dropdown.configure(width=130, height=40, font=(self.textFont, 16), dropdown_font=(self.textFont, 16))

    def toggle_transmission(self):
        if self.cap is None:
            selected_camera_index = self.camera_list.index(self.camera_var.get())
            self.cap = cv2.VideoCapture(selected_camera_index)
            self.update_frame()  # Iniciar la transmisión
            self.toggle_transmission_button.configure(text="Detener Transmisión")
        else:
            self.stop_transmission()  # Detener la transmisión
            self.toggle_transmission_button.configure(text="Iniciar Transmisión")

    def stop_transmission(self):
        if self.cap is not None:
            self.cap.release()  # Libera la captura de la cámara
            self.cap = None
            self.lblInputImage1.configure(image=None)

    def get_camera_list(self):
        # Obtener una lista de cámaras disponibles
        camera_list = []
        for i in range(10):  # Suponemos que hay 10 cámaras como máximo
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(f"Cámara {i + 1}")
                cap.release()
        return camera_list
    
    def exportar_excel(self):
        df = pd.read_excel("prueba.xlsx")
        df.to_excel("COPIADO.xlsx")
        print(df.head(5))
    
    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (400, 400))
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lblInputImage1.imgtk = imgtk
                self.lblInputImage1.configure(image=imgtk)
                self.frame.after(10, self.update_frame)

    def volver(self):
        self.stop_transmission()  # Asegurarse de detener la transmisión antes de cambiar de página
        self.hide()
        self.master.show_abrir_archivo_page()

    def update_widgets_font_and_size(self):
        # Actualizar la fuente y el tamaño de letra de los widgets en esta página
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize

        self.text.configure(font=(self.textFont, self.fontSize + 12))
        self.lblInfo3.configure(font=(self.textFont, self.fontSize))
        self.lblInfo4.configure(font=(self.textFont, self.fontSize))
        self.lblInfo5.configure(font=(self.textFont, self.fontSize))
        self.volver_button.configure(font=(self.textFont, self.fontSize))