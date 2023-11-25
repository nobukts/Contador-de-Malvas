from tkinter import *
import customtkinter
from page import Page
from settings import app_settings
import cv2
from PIL import Image, ImageTk
import pandas as pd
from ultralytics import YOLO
from datetime import datetime
from tkinter import messagebox

#Cargar el modelo
model = YOLO("TrainModelMalva.pt")

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
        self.rootAnalisis.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)

        # Pantalla de inicio
        self.toggle_transmission_button = customtkinter.CTkButton(self.root, text="Iniciar Transmisión", width=25, command=self.toggle_transmission)
        self.toggle_transmission_button.grid(row=1, column=0)

        self.lblInputImage1 = customtkinter.CTkLabel(self.root, text="")
        self.lblInputImage1.grid(row=0, column=0)

        self.text = customtkinter.CTkLabel(self.rootAnalisis, text="Análisis", font=(self.textFont, self.fontSize+12))
        self.text.grid(column=0, pady=10)

        self.lblInfo3 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas buenas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo3.grid(row=1, pady=15, padx=5)
        self.lblInfo4 = customtkinter.CTkLabel(self.rootAnalisis, text="Cantidad de malvas malas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo4.grid(row=2, pady=5, padx=5)
        self.lblInfo5 = customtkinter.CTkLabel(self.rootAnalisis, text="Porcentaje de malvas buenas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo5.grid(row=3, pady=15, padx=5)
        self.lblInfo7 = customtkinter.CTkLabel(self.rootAnalisis, text="Porcentaje de malvas malas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo7.grid(row=4, pady=5, padx=5)
        self.lblInfo8 = customtkinter.CTkLabel(self.rootAnalisis, text="Total de malvas: 0", font=(self.textFont, self.fontSize), fg_color=("#c8c8c8","#3a3a3a"), text_color=("black","white"), padx=10)
        self.lblInfo8.grid(row=5, pady=15, padx=5)
        self.lblInfo6 = customtkinter.CTkButton(self.rootAnalisis, text="Exportar excel", command=self.exportar_excel)
        self.lblInfo6.grid(row=6, pady=5)
        
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

        #self.master.protocol("WM_DELETE_WINDOW",self.on_closing)

    def toggle_transmission(self):
        #Definir variables
        global contMalvaBuena, contMalvaMala
        global flag_export
        flag_export = True

        if self.cap is None:
            contMalvaBuena = []
            contMalvaMala = []
            #guardar tiempo de inicio
            global start_datetime
            flag_export = False
            start_datetime = datetime.now()

            selected_camera_index = self.camera_list.index(self.camera_var.get())
            self.cap = cv2.VideoCapture(selected_camera_index)
            self.update_frame()  # Iniciar la transmisión
            self.toggle_transmission_button.configure(text="Detener Transmisión")
        else:
            flag_export = True
            self.stop_transmission()  # Detener la transmisión
            self.toggle_transmission_button.configure(text="Iniciar Transmisión")
            #guardar tiempo final
            global finish_datetime
            finish_datetime = datetime.now()

    def stop_transmission(self):
        if self.cap is not None:
            self.cap.release()  # Libera la captura de la cámara
            self.cap = None
            self.lblInputImage1.configure(image=None)

    def get_camera_list(self):
        # Obtener una lista de cámaras disponibles
        camera_list = []
        for i in range(3):  # Suponemos que hay 10 cámaras como máximo
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_list.append(f"Cámara {i + 1}")
                cap.release()
        return camera_list
    
    def exportar_excel(self):
        try:
            if flag_export:
                #Exportar excel cuando la transmisión esté detenida
                
                try:
                    finish_time = finish_datetime.strftime("%H:%M:%S")
                    finish_date = finish_datetime.strftime("%d-%m-%Y")
                    start_time = start_datetime.strftime("%H:%M:%S")
                    start_date = start_datetime.strftime("%d-%m-%Y")
                    df = pd.read_excel('./exportado.xlsx', index_col=0)
                    datos = pd.DataFrame([{'fecha inicio':start_date,'hora inicio':start_time,'fecha final':finish_date,'hora final':finish_time,'Buenas':len(contMalvaBuena),'Malas':len(contMalvaMala),'Total':totalMalvas,'%buenas':porcentajeBuenas,'%malas':porcentajeMalas,'Tipo':'Transmision'}])
                    df = pd.concat([df, datos], ignore_index=True)
                    df.to_excel("./exportado.xlsx")
                    messagebox.showinfo(title="Exportado correctamente",message="Se ha exportado correctamente")
                    print(df)
                except Exception as e:
                    print("Surgió un error al exportar el excel")
                    messagebox.showerror(title="Exportado incorrectamente",message="Hubo un problema al exportar el excel")
            else:
                messagebox.showerror(title="Exportado incorrectamente",message="Detenga la transmisión para poder exportar el excel")
            
        except Exception as e:
            messagebox.showerror(title="Exportado incorrectamente",message="Hubo un problema al exportar el excel")
    
    def update_frame(self):

        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                
                #Uso del modelo
                results = model.track(frame, persist=True, conf=0.8)

                frame_ = results[0].plot()

                #Limit line
                line_height, line_width, _ = frame.shape
                limits = [0,int(line_height/2),line_width,int(line_height/2)]

                #cv2.line(frame_,(limits[0],limits[1]),(limits[2],limits[3]),(0,0,255),5)

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

                frame = cv2.resize(frame_, (400, 400))
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lblInputImage1.imgtk = imgtk
                self.lblInputImage1.configure(image=imgtk)
                self.frame.after(10, self.update_frame)

                global porcentajeBuenas, porcentajeMalas, totalMalvas
                try:
                    totalMalvas = len(contMalvaBuena) + len(contMalvaMala)
                    porcentajeBuenas = 100*len(contMalvaBuena)/totalMalvas
                    porcentajeMalas = 100*len(contMalvaMala)/totalMalvas
                    porcentajeBuenas = round(porcentajeBuenas, 2)
                    porcentajeMalas = round(porcentajeMalas, 2)
                except Exception as e:
                    print("Error al calcular el porcentaje")
                    porcentajeBuenas = 0
                    porcentajeMalas = 0
                
                #Insertar texto correspondiente a la video
                self.lblInfo3.configure(text=f"Cantidad de malvas buenas: {len(contMalvaBuena)}")
                self.lblInfo4.configure(text=f"Cantidad de malvas malas: {len(contMalvaMala)}")
                self.lblInfo5.configure(text=f"Porcentaje de malvas buenas: {porcentajeBuenas}%")
                self.lblInfo7.configure(text=f"Porcentaje de malvas malas: {porcentajeMalas}%")
                self.lblInfo8.configure(text=f"Total de malvas: {len(contMalvaBuena)+len(contMalvaMala)}")

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
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()