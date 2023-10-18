from tkinter import *
import customtkinter
from page import Page
from settings import app_settings
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import pandas as pd
import cv2
from datetime import datetime
from ultralytics import YOLO

#Cargar el modelo
model = YOLO("TrainModelMalva.pt")

class AnalisisVideoPage(Page):
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

        #Configurar analisis
        self.rootAnalisis = customtkinter.CTkFrame(self.root, width=140, corner_radius=0)
        self.rootAnalisis.grid(row=0, rowspan=2, column=1)
        self.rootAnalisis.grid_rowconfigure((0,1,2,3,4,5), weight=1)

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

        #Configurar video
        self.rootZonaVideo = customtkinter.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.rootZonaVideo.grid(row=0, rowspan=2, column=0, ipadx=130, ipady=80)

        self.lblInputVideo1 = TkinterVideo(self.rootZonaVideo)
        

        self.cell1 = customtkinter.CTkButton(self.rootZonaVideo, text="Elegir video", width=25, command=self.elegir_video)
        self.cell1.pack(pady=10, side=BOTTOM)

        self.cell2 = customtkinter.CTkButton(self.rootZonaVideo, text="Recargar", width=25, command=self.recargar)

        self.error = customtkinter.CTkLabel(self.rootAnalisis, text="Primero debe analizar foto")

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(self.textFont, self.fontSize), command=self.volver, fg_color='dark red')
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
            out = cv2.VideoWriter(output_path, fourcc, fps * 1, (frame_width, frame_height))

            #Definir variables
            global contMalvaBuena, contMalvaMala
            contMalvaBuena = []
            contMalvaMala = []

            #Limit line
            limits = [10,300,800,300]

            #definir punto de inicio y fin de linea a dibujar
            #startPoint = (0, frame_height // 2)
            #endPoint = (frame_width//8, (frame_height // 2))

            while cap.isOpened():
                ret, frameVideo = cap.read()
                if not ret:
                    break
                
                #Uso del modelo
                results = model.track(frameVideo, persist=True, conf=0.8)

                frame_ = results[0].plot()

                cv2.line(frame_,(limits[0],limits[1]),(limits[2],limits[3]),(0,0,255),5)

                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        classMalvas = int(box.cls)
                        if box.id:
                            id = int(box.id)

                        w, h = x2-x1, y2-y1
                        cx, cy = x1+w//2, y1+h//2

                        cv2.circle(frame_, (cx,cy),5,(255,0,255),cv2.FILLED)

                        if limits[0] < cx < limits[2] and limits[1] - 20 < cy < limits[3] + 20:
                            if classMalvas == 0:
                                if contMalvaBuena.count(id) == 0:
                                    contMalvaBuena.append(id)
                            else:
                                if contMalvaMala.count(id) == 0:
                                    contMalvaMala.append(id)
                
                
                # Resto del código de procesamiento e inferencia
                #response = model.predict(frameVideo, confidence=70, overlap=30).json()

                # Write the frame with bounding boxes to the output video
                out.write(frame_)


            # Release the capture and output objects
            cap.release()
            out.release()

            #Prints (Eliminar)
            print("La cantidad de malvas buenas es: " + str(len(contMalvaBuena)))
            print("La cantidad de malvas malas es: " + str(len(contMalvaMala)))
            print("La cantidad de malvas es: " + str(len(contMalvaMala)+len(contMalvaBuena)))

            self.cell2.pack(pady=10, side=BOTTOM)
            #Cargar video y reproducirlo
            self.lblInputVideo1.load("./"+output_path)
            self.lblInputVideo1.play()

            #Insertar texto correspondiente a la video
            self.lblInfo3.configure(text=f"Cantidad de malvas buenas: {len(contMalvaBuena)}")
            self.lblInfo4.configure(text=f"Cantidad de malvas malas: {len(contMalvaMala)}")
            self.lblInfo5.configure(text=f"Cantidad de malvas por minuto: {0}")

        #Eliminando variables
        del cap
        del out
        del frame_
        del results
        del ret
        del frameVideo
        del fourcc
        del output_path

    def recargar(self):
        self.lblInputVideo1.play()

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
        self.lblInfo5.configure(font=(self.textFont, self.fontSize))
        self.volver_button.configure(font=(self.textFont, self.fontSize))