from tkinter import *
import customtkinter
from cargarConfig import loadConfiguration
from tkinter import filedialog
import cv2
import imutils
from PIL import Image, ImageTk

class AnalisisVideo(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Load configuration
        textFont, fontSize, darkMode = loadConfiguration()

        #Configure windows
        self.title("Analisis de video.py")
        self.geometry(f"{850}x{650}")
        self.minsize(600,350)
        
        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.root = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.root.grid(row=1, column=1, sticky="nsew")
        self.root.grid_columnconfigure((0,1),weight=1)
        self.root.grid_rowconfigure((0,1), weight=1)

        self.rootAnalisis = customtkinter.CTkFrame(self.root, width=140, corner_radius=0)
        self.rootAnalisis.grid(row=0, rowspan=2, column=1)
        self.rootAnalisis.grid_rowconfigure((0,1,2,3), weight=1)

        #Pantalla de inicio
        self.cell1 = customtkinter.CTkButton(self.root, text="Elegir video", width=25, command=self.elegir_video)
        self.cell1.grid(row=1, column=0)

        self.lblInputVideo1 = customtkinter.CTkLabel(self.root, text="")
        self.lblInputVideo1.grid(row=0, column=0)

        self.text = customtkinter.CTkLabel(self.rootAnalisis, text="Análisis", font=(textFont,fontSize+12))
        self.text.grid(column=0, pady=10)

        self.lblInfo3 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo3.grid(row=1, pady=15, padx=5)
        self.lblInfo4 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas volteadas: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo4.grid(row=2, pady=5, padx=5)
        self.lblInfo5 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas por minuto: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo5.grid(row=3, pady=15, padx=5)
        
        self.mainloop()
    
    def elegir_video(self):
        path_video = filedialog.askopenfilename(filetypes=[("video", ".mp4"),
                                                        ("video", ".mkv"),
                                                        ("video",".avi")])
        if len(path_video) > 0:
            """ #Se comenta porque se hará de distinta forma para la colocacion de un video
            #obtención de video
            video = cv2.imread(path_video)

            #redimensionar video
            video = imutils.resize(video, height=500)

            #redimensionar video que se va colocar en la ventana
            videoToShow = imutils.resize(video, width=300)

            #cambiar paleta de colores para utilizar en la ventana
            videoToShow = cv2.cvtColor(videoToShow, cv2.COLOR_BGR2RGB)

            #guardar resultados en variables para mostrar en la ventana
            vid = Image.fromarray(videoToShow)
            img = ImageTk.PhotoImage(video=vid, size=(30,30))

            #insertar video en la ventana
            self.lblInputVideo1.configure(video=img)
            self.lblInputVideo1.video = img """

            #Insertar texto correspondiente a la video
            self.lblInfo3.configure(text=f"Cantidad de malvas: {0}")
            self.lblInfo4.configure(text=f"Cantidad de malvas volteadas: {0}")
            self.lblInfo5.configure(text=f"Cantidad de malvas por minuto: {0}")