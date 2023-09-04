from tkinter import *
import customtkinter
from page import Page
from cargarConfig import loadConfiguration
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import pandas as pd
import cv2
from roboflow import Roboflow
from datetime import datetime
from apikey import api_key

#Cargar el roboflow
rf = Roboflow(api_key)
project = rf.project("malvas")
model = project.version(5).model

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
        self.rootAnalisis.grid_rowconfigure((0,1,2,3,4,5), weight=1)

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

        self.cell2 = customtkinter.CTkButton(self.rootZonaVideo, text="Recargar", width=25, command=self.recargar)

        self.error = customtkinter.CTkLabel(self.rootAnalisis, text="Primero debe analizar foto")

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(textFont, fontSize), command=self.volver, fg_color='dark red')
        self.volver_button.grid(row=2, column=1, pady=30)
        
    
    def exportar_excel(self):
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d-%m-%Y")
            df = pd.read_excel('exportado.xlsx', index_col=0)
            datos = pd.DataFrame([{'fecha':current_date,'hora':current_time,'Buenas':contMalvaBuena,'Malas':contMalvaMala}])
            df = pd.concat([df, datos], ignore_index=True)
            df.to_excel("exportado.xlsx")
            self.error.grid_forget()
            print(df)
        except Exception as e:
            print("Primero analice la foto")
            self.error.grid(row=5)
    
    def elegir_video(self):
        path_video = filedialog.askopenfilename(filetypes=[("video", ".mp4"),
                                                        ("video", ".mkv"),
                                                        ("video",".avi")])
        self.lblInputVideo1.pack(expand=True, fill="both")
        if len(path_video) > 0:
            #Cargar el video
            cap = cv2.VideoCapture(path_video)
            self.lblInputVideo1.pack(expand=True, fill="both")

            # Get video properties
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            fps = int(cap.get(5))

            #Exportar video (eliminar)
            # Define the codec and create VideoWriter object to save the output
            output_path = "videoFinal.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps * 0.1, (frame_width, frame_height))

            #Definir variables
            global contMalvaBuena, contMalvaMala
            contMalvaMala = 0 
            contMalvaBuena = 0
            contFrame = 0
            contMalva = 0
            font = cv2.FONT_HERSHEY_TRIPLEX

            #frames_to_skip = 10  # Analizar cada n fotograma
            frames_to_skip = 15
            frame_counter = 0

            #definir punto de inicio y fin de linea a dibujar
            #startPoint = (0, frame_height // 2)
            #endPoint = (frame_width//8, (frame_height // 2))

            while cap.isOpened():
                ret, frameVideo = cap.read()
                if not ret:
                    break
                
                frame_counter += 1
                if frame_counter % frames_to_skip != 0:
                    continue
                
                #cv2.line(frame, startPoint, endPoint, (255,0,0),1) #(imagen,(x1,y1),(x2,y2),(B,G,R),grosor) funcion para dibujar rectangulos en la imagen

                # Resto del código de procesamiento e inferencia
                response = model.predict(frameVideo, confidence=70, overlap=30).json()

                # Resto del código de dibujo de cajas y recuento de malvas
                for pred in response['predictions']: #recorrer el json de predictions
                    contFrame = contFrame + 1
                    x1 = int(pred['x'] - pred['width'] / 2)
                    y1 = int(pred['y'] - pred['height'] / 2)

                    x2 = int(x1 + pred['width'])
                    y2 = int(y1 + pred['height'])
                
                    if pred['class'] == 'malvaBuena': 
                        cv2.rectangle(frameVideo,(x1,y1),(x2,y2),(0,102,0),1)#(imagen,(x1,y1),(x2,y2),(B,G,R),grosor) funcion para dibujar rectangulos en la imagen
                        cv2.putText(frameVideo, 'malvaBuena', (x1,y1-5), font,1,(0,102,0),2,cv2.LINE_AA) #funcion para escribir texto en la imagen
                        #contMalvaBuena = contMalvaBuena + 1
                        if y1 <= (frame_height // 2) and y2 >= (frame_height // 2):
                            contMalvaBuena += 1

                    if pred['class'] == 'malvaMala':
                        cv2.rectangle(frameVideo,(x1,y1),(x2,y2),(0,0,255),1)
                        cv2.putText(frameVideo, 'malvaMala', (x1,y1-5), font,1,(0,0,255),2,cv2.LINE_AA)
                        #contMalvaMala = contMalvaMala + 1
                        if y1 <= (frame_height // 2) and y2 >= (frame_height // 2):
                            contMalvaMala += 1

                    if y1 <= (frame_height // 2) and y2 >= (frame_height // 2):
                        contMalva += 1

                
                cv2.putText(frameVideo, f'Malvas buenas: {contMalvaBuena}', (10,30), font,1,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(frameVideo, f'Malvas malas: {contMalvaMala}', (10,60), font,1,(0,0,0),2,cv2.LINE_AA)
                # Write the frame with bounding boxes to the output video
                out.write(frameVideo)


            # Release the capture and output objects
            cap.release()
            out.release()

            #Prints (Eliminar)
            print("La cantidad de malvas buenas es: " + str(contMalvaBuena))
            print("La cantidad de malvas malas es: " + str(contMalvaMala))
            print("La cantidad de malvas es: " + str(contMalva))
            print("La cantidad de frames es: " + str(contFrame))

            self.cell2.pack(pady=10, side=BOTTOM)
            #Cargar video y reproducirlo
            self.lblInputVideo1.load(path_video)
            self.lblInputVideo1.play()

            #Insertar texto correspondiente a la video
            self.lblInfo3.configure(text=f"Cantidad de malvas buenas: {contMalvaBuena}")
            self.lblInfo4.configure(text=f"Cantidad de malvas malas: {contMalvaMala}")
            self.lblInfo5.configure(text=f"Cantidad de malvas por minuto: {0}")

    def recargar(self):
        self.lblInputVideo1.play()

    def volver(self):
        self.hide()
        self.master.show_abrir_archivo_page() 