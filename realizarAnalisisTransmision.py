from tkinter import *
import customtkinter
from cargarConfig import loadConfiguration
from tkinter import filedialog
import cv2
import imutils
from PIL import Image, ImageTk

class AnalisisTransmision(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Load configuration
        textFont, fontSize, darkMode = loadConfiguration()

        #Configure windows
        self.title("Analisis de transmision.py")
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
        self.cell1 = customtkinter.CTkButton(self.root, text="Detectando camara...", width=25, command=self.elegir_video)
        self.cell1.grid(row=1, column=0)

        self.lblInputImage1 = customtkinter.CTkLabel(self.root, text="")
        self.lblInputImage1.grid(row=0, column=0)

        self.lblInputImage2 = customtkinter.CTkLabel(self.root, text="")
        self.lblInputImage2.grid(row=0, column=0)

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
        #Todo esto deberia cambiar al ser una transmision en vivo
        path_image = filedialog.askopenfilename(filetypes=[("image", ".jpg"),
                                                        ("image", ".jpeg"),
                                                        ("image",".png")])
        if len(path_image) > 0:
            #obtención de imagen
            image = cv2.imread(path_image)
            imagen = image

            #redimensionar imagen
            image = imutils.resize(image, height=500)
            imagen = imutils.resize(imagen, height=500)

            #redimensionar imagen que se va colocar en la ventana
            imageToShow = imutils.resize(image, width=300)
            imageToShow2 = imutils.resize(imagen, width=300)

            #cambiar paleta de colores para utilizar en la ventana
            imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB) 
            imageToShow2 = cv2.cvtColor(imageToShow2, cv2.COLOR_BGR2RGB)

            #generar bordes de la imagen a analizar
            bordes = cv2.Canny(imageToShow2, 100, 600)
            contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #dibujar contornos en la imagen
            cv2.drawContours(imageToShow2, contornos, -1, (0, 255, 0), 2)

            #guardar resultados en variables para mostrar en la ventana
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im, size=(30,30))
            im2 = Image.fromarray(imageToShow2)
            img2 = ImageTk.PhotoImage(image=im2, size=(30,30))

            #insertar imagen en la ventana
            self.lblInputImage1.configure(image=img)
            self.lblInputImage1.image = img
            self.lblInputImage2.configure(image=img2)
            self.lblInputImage2.image = img2

            #Insertar texto correspondiente a la imagen
            self.lblInfo3.configure(text=f"Cantidad de malvas: {len(contornos)}")
            self.lblInfo4.configure(text=f"Cantidad de malvas volteadas: {len(contornos)}")
            self.lblInfo5.configure(text=f"Cantidad de malvas por minuto: {len(contornos)}")