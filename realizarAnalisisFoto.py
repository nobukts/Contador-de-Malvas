import customtkinter
from page import Page
from cargarConfig import loadConfiguration
from tkinter import filedialog
import cv2
import imutils
from PIL import Image, ImageTk
import pandas as pd
from roboflow import Roboflow
from datetime import datetime
from apikey import api_key

#Cargar el roboflow
rf = Roboflow(api_key)
project = rf.project("malvas")
model = project.version(5).model

class AnalisisFotoPage(Page):
    def __init__(self, master):
        super().__init__(master)
        textFont, fontSize, darkMode = loadConfiguration()
        
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.root = customtkinter.CTkFrame(self.frame, width=140, corner_radius=0)
        self.root.grid(row=1, column=1, sticky="nsew")
        self.root.grid_columnconfigure((0,1),weight=1)
        self.root.grid_rowconfigure((0,1), weight=1)

        self.rootAnalisis = customtkinter.CTkFrame(self.root, width=140, corner_radius=0)
        self.rootAnalisis.grid(row=0, rowspan=2, column=1)
        self.rootAnalisis.grid_rowconfigure((0,1,2,3,4), weight=1)

        #Pantalla de inicio
        self.cell1 = customtkinter.CTkButton(self.root, text="Cambiar foto", width=25, command=self.elegir_imagen)
        self.cell1.grid(row=1, column=0)

        self.lblInputImage1 = customtkinter.CTkLabel(self.root, text="")
        self.lblInputImage1.grid(row=0, column=0)

        self.text = customtkinter.CTkLabel(self.rootAnalisis, text="Análisis", font=(textFont,fontSize+12))
        self.text.grid(column=0, pady=10)

        self.lblInfo3 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas buenas: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo3.grid(row=1, pady=5, padx=5)
        self.lblInfo4 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas malas: 0", font=(textFont,fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo4.grid(row=2, pady=15, padx=5)
        self.lblInfo6 = customtkinter.CTkButton(self.rootAnalisis, text="Exportar excel", command=self.exportar_excel)
        self.lblInfo6.grid(row=3, pady=5)

        self.error = customtkinter.CTkLabel(self.rootAnalisis, text="Primero debe analizar foto")

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(textFont, fontSize), command=self.volver, fg_color='dark red')
        self.volver_button.grid(row=2, column=1, pady=30)

    def exportar_excel(self):
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d-%m-%Y")
            df = pd.read_excel('../../exportado.xlsx', index_col=0)
            datos = pd.DataFrame([{'fecha':current_date,'hora':current_time,'Buenas':contMalvaBuena,'Malas':contMalvaMala}])
            df = pd.concat([df, datos], ignore_index=True)
            df.to_excel("../../exportado.xlsx")
            self.error.grid_forget()
            print(df)
        except Exception as e:
            print("Primero analice la foto")
            self.error.grid(row=4)
        
    
    def elegir_imagen(self):
        path_image = filedialog.askopenfilename(filetypes=[("image", ".jpg"),
                                                        ("image", ".jpeg"),
                                                        ("image",".png")])
        if len(path_image) > 0:
            global contMalvaBuena, contMalvaMala
            #obtención de imagen
            imagen = cv2.imread(path_image)

            response = model.predict(path_image, confidence=80, overlap=30).json() #json en donde estan las predicciones del modelo

            contMalvaMala = 0
            contMalvaBuena = 0
            font = cv2.FONT_HERSHEY_TRIPLEX

            for pred in response['predictions']: #recorrer el json de predictions

                x1 = pred['x'] - int(pred['width']/2) #coordenada X en donde empieza se empieza a dibujar el rectangulo para seleccionar malva 
                y1 = pred['y'] - int(pred['height']/2) #coordenada Y en donde empieza se empieza a dibujar el rectangulo para seleccionar malva 

                x2 = x1 + pred['width'] #coordenada X en donde empieza se termina de dibujar el rectangulo para seleccionar malva 
                y2 = y1 + pred['height'] #coordenada Y en donde empieza se termina de dibujar el rectangulo para seleccionar malva 
                
                if pred['class'] == 'malvaBuena': 
                    cv2.rectangle(imagen,(x1,y1),(x2,y2),(0,102,0),3)#(imagen,(x1,y1),(x2,y2),(B,G,R),grosor) funcion para dibujar rectangulos en la imagen
                    cv2.putText(imagen, 'malvaBuena', (x1,y1-5), font,0.75,(0,102,0),2,cv2.LINE_AA) #funcion para escribir texto en la imagen
                    contMalvaBuena = contMalvaBuena + 1

                if pred['class'] == 'malvaMala':
                    cv2.rectangle(imagen,(x1,y1),(x2,y2),(0,0,255),3)#(imagen,(x1,y1),(x2,y2),(B,G,R),grosor)
                    cv2.putText(imagen, 'malvaMala', (x1,y1-5), font,0.75,(0,0,255),2,cv2.LINE_AA)
                    contMalvaMala = contMalvaMala + 1
            
            self.lblInfo3.configure(text=f"Cantidad de malvas buenas: {contMalvaBuena}")
            self.lblInfo4.configure(text=f"Cantidad de malvas malas: {contMalvaMala}")

            """ cv2.imwrite("fotos/rectangulos1.jpg", imagen) """ #funcion para guardar la imagen en la ruta especificada
            
            imageToShow2 = imutils.resize(imagen, width=500)
            imageToShow2 = cv2.cvtColor(imageToShow2, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(imageToShow2)
            img = ImageTk.PhotoImage(image=im, size=(30,30))

            self.lblInputImage1.configure(image=img)


    def volver(self):
        self.hide()
        self.master.show_abrir_archivo_page() 
