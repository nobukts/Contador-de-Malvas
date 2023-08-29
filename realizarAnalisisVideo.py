from tkinter import *
import customtkinter
from page import Page
from cargarConfig import loadConfiguration
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import pandas as pd

class AnalisisVideoPage(Page):
    def __init__(self,master):
        super().__init__(master)

        #Load configuration
        textFont, fontSize, darkMode = loadConfiguration()

        #Configure windows
        # self.title("Analisis de video.py")
        # self.geometry(f"{850}x{650}")
        # self.minsize(600,350)
        
        # configure grid layout (4x4)
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.root = customtkinter.CTkFrame(self.frame, width=140, corner_radius=0)
        self.root.grid(row=1, column=1, sticky="nsew")
        self.root.grid_columnconfigure((0,1),weight=1)
        self.root.grid_rowconfigure((0,1), weight=1)

        #Configurar analisis
        self.rootAnalisis = customtkinter.CTkFrame(self.root, width=140, corner_radius=0)
        self.rootAnalisis.grid(row=0, rowspan=2, column=1)
        self.rootAnalisis.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.text = customtkinter.CTkLabel(self.rootAnalisis, text="Análisis", font=(textFont,fontSize+12))
        self.text.grid(column=0, pady=10)

        self.lblInfo3 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo3.grid(row=1, pady=15, padx=5)
        self.lblInfo4 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas volteadas: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo4.grid(row=2, pady=5, padx=5)
        self.lblInfo5 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas por minuto: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo5.grid(row=3, pady=15, padx=5)
        self.lblInfo6 = customtkinter.CTkButton(self.rootAnalisis, text="Exportar excel", command=self.exportar_excel)
        self.lblInfo6.grid(row=4, pady=5)

        #Configurar video
        self.rootZonaVideo = customtkinter.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.rootZonaVideo.grid(row=0, rowspan=2, column=0, ipadx=130, ipady=80)

        self.lblInputVideo1 = TkinterVideo(self.rootZonaVideo)
        

        self.cell1 = customtkinter.CTkButton(self.rootZonaVideo, text="Elegir video", width=25, command=self.elegir_video)
        self.cell1.pack(pady=10, side=BOTTOM)

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(textFont, fontSize), command=self.volver, fg_color='dark red')
        self.volver_button.grid(row=2, column=1, pady=30)
        
    
    def exportar_excel(self):
        df = pd.read_excel("prueba.xlsx")
        df.to_excel("COPIADO.xlsx")
        print(df.head(5))
    
    def elegir_video(self):
        path_video = filedialog.askopenfilename(filetypes=[("video", ".mp4"),
                                                        ("video", ".mkv"),
                                                        ("video",".avi")])
        self.lblInputVideo1.pack(expand=True, fill="both")
        if len(path_video) > 0:
            #Cargar video y reproducirlo
            self.lblInputVideo1.load(path_video)
            self.lblInputVideo1.play()
            

            #Insertar texto correspondiente a la video
            self.lblInfo3.configure(text=f"Cantidad de malvas: {0}")
            self.lblInfo4.configure(text=f"Cantidad de malvas volteadas: {0}")
            self.lblInfo5.configure(text=f"Cantidad de malvas por minuto: {0}")

    def volver(self):
        self.hide()
        self.master.show_abrir_archivo_page() 