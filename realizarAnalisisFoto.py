import customtkinter
from page import Page
from tkinter import filedialog, messagebox
import cv2
import imutils
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime
from settings import app_settings
from ultralytics import YOLO
import time

#Cargar el modelo
model = YOLO("TrainModelMalva.pt")

class AnalisisFotoPage(Page):
    def __init__(self, master):
        super().__init__(master)
        app_settings.load_configuration()
        
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize

        self.root = customtkinter.CTkFrame(self.frame, width=140, corner_radius=0)
        self.root.grid(row=1, column=1, sticky="nsew")
        self.root.grid_columnconfigure((0, 1), weight=1)
        self.root.grid_rowconfigure((0, 1), weight=1)

        self.rootAnalisis = customtkinter.CTkFrame(self.root, width=140, corner_radius=0)
        self.rootAnalisis.grid(row=0, rowspan=2, column=1)
        self.rootAnalisis.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Pantalla de inicio
        self.cell1 = customtkinter.CTkButton(self.root, text="Cambiar foto", width=25, command=self.elegir_imagen)
        self.cell1.grid(row=1, column=0)

        self.lblInputImage1 = customtkinter.CTkLabel(self.root, text="")
        self.lblInputImage1.grid(row=0, column=0)

        self.text = customtkinter.CTkLabel(self.rootAnalisis, text="Análisis", font=(self.textFont, self.fontSize + 12))
        self.text.grid(column=0, pady=10)

        self.lblInfo3 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas buenas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8", "#3a3a3a"), text_color=("black", "white"), padx=10)
        self.lblInfo3.grid(row=1, pady=15, padx=5)
        self.lblInfo4 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas malas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8", "#3a3a3a"), text_color=("black", "white"), padx=10)
        self.lblInfo4.grid(row=2, pady=5, padx=5)
        self.lblInfo5 = customtkinter.CTkLabel(self.rootAnalisis, text="Porcentaje de malvas buenas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo5.grid(row=3, pady=15, padx=5)
        self.lblInfo7 = customtkinter.CTkLabel(self.rootAnalisis, text="Porcentaje de malvas malas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo7.grid(row=4, pady=5, padx=5)
        self.lblInfo6 = customtkinter.CTkButton(self.rootAnalisis, text="Exportar excel", command=self.exportar_excel)
        self.lblInfo6.grid(row=5, pady=15)

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(self.textFont, self.fontSize), command=self.volver, fg_color='dark red')
        self.volver_button.grid(row=2, column=1, pady=30)

    def exportar_excel(self):

        try:
            now = datetime.now()
            finish_time = now.strftime("%H:%M:%S")
            finish_date = now.strftime("%d-%m-%Y")
            df = pd.read_excel('./exportado.xlsx', index_col=0)
            datos = pd.DataFrame([{'fecha inicio':finish_date,'hora inicio':finish_time,'fecha final':finish_date,'hora final':finish_time,'Buenas':contMalvaBuena,'Malas':contMalvaMala,'Total':totalMalvas,'%buenas':porcentajeBuenas,'%malas':porcentajeMalas,'Tipo':'Foto'}])
            df = pd.concat([df, datos], ignore_index=True)
            df.to_excel("./exportado.xlsx")
            messagebox.showinfo(title="Exportado correctamente",message="Se ha exportado correctamente")
            print(df)
        except Exception as e:
            print("Surgió un error al exportar el excel")
            messagebox.showerror(title="Exportado incorrectamente",message="Hubo un problema al exportar el excel")
        
    
    def elegir_imagen(self):
        path_image = filedialog.askopenfilename(filetypes=[("image", ".jpg"),
                                                        ("image", ".jpeg"),
                                                        ("image",".png")])
        if len(path_image) > 0:
            global contMalvaBuena, contMalvaMala
            global porcentajeBuenas, porcentajeMalas, totalMalvas
            contMalvaMala = 0
            contMalvaBuena = 0
            #obtención de imagen
            imagen = cv2.imread(path_image)

            results = model([imagen])

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    classMalvas = int(box.cls)

                    #Dibujar
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2-x1, y2-y1
                    cx, cy = x1+w//2, y1+h//2
                    
                    max_y = y1-27
                    if max_y < 0:
                        max_y = y1-max_y
                    else:
                        max_y = y1
                    if classMalvas == 0:
                        cv2.rectangle(imagen, (x1, y1), (x2, y2), (8,75,255), thickness=2) #Marca de la malva
                        cv2.rectangle(imagen, (x1, max_y+3), (x1+200, max_y-27), (8,75,255), thickness=cv2.FILLED) #Rellenar fondo del texto
                        cv2.putText(imagen, "Malva buena", (x1, max_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4) #Texto
                        contMalvaBuena += 1
                    else:
                        cv2.rectangle(imagen, (x1, y1), (x2, y2), (0,0,255), thickness=2)
                        cv2.rectangle(imagen, (x1, max_y+3), (x1+175, max_y-27), (0,0,255), thickness=cv2.FILLED) #Rellenar fondo del texto
                        cv2.putText(imagen, "Malva Mala", (x1, max_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)
                        contMalvaMala += 1
            
            imageToShow2 = imutils.resize(imagen, width=500)
            imageToShow2 = cv2.cvtColor(imageToShow2, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(imageToShow2)
            img = ImageTk.PhotoImage(image=im, size=(30,30))

            try:
                totalMalvas = contMalvaBuena+contMalvaMala
                porcentajeBuenas = 100*contMalvaBuena/totalMalvas
                porcentajeMalas = 100*contMalvaMala/totalMalvas
                porcentajeBuenas = round(porcentajeBuenas, 2)
                porcentajeMalas = round(porcentajeMalas, 2)
            except Exception as e:
                print("Error al calcular el porcentaje")
                porcentajeBuenas = 0
                porcentajeMalas = 0
            
            self.lblInfo3.configure(text=f"Cantidad de malvas buenas: {contMalvaBuena}")
            self.lblInfo4.configure(text=f"Cantidad de malvas malas: {contMalvaMala}")
            self.lblInfo5.configure(text=f"Porcentaje de malvas buenas: {porcentajeBuenas}%")
            self.lblInfo7.configure(text=f"Porcentaje de malvas malas: {porcentajeMalas}%")

            self.lblInputImage1.configure(image=img)


    def volver(self):
        self.hide()
        self.master.show_abrir_archivo_page() 

    def update_widgets_font_and_size(self):
        # Actualizar la fuente y el tamaño de letra de los widgets en esta página
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize

        self.text.configure(font=(self.textFont, self.fontSize + 12))
        self.lblInfo3.configure(font=(self.textFont, self.fontSize))
        self.lblInfo4.configure(font=(self.textFont, self.fontSize))
        self.volver_button.configure(font=(self.textFont, self.fontSize))
