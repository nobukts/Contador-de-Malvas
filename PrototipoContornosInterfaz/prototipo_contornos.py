# Import required libraries
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np

def elegir_imagen():
    path_image = filedialog.askopenfilename(filetypes=[("image", ".jpg"),
                                                       ("image", ".jpeg"),
                                                       ("image",".png")])
    if len(path_image) > 0:
        global image
        #obtención de imagen
        image = cv2.imread(path_image)
        imagen = image

        #redimensionar imagen
        image = imutils.resize(image, height=500)
        imagen = imutils.resize(imagen, height=500)

        #redimensionar imagen que se va colocar en la ventana
        imageToShow = imutils.resize(image, width=500)
        imageToShow2 = imutils.resize(imagen, width=500)

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
        img = ImageTk.PhotoImage(image=im)
        im2 = Image.fromarray(imageToShow2)
        img2 = ImageTk.PhotoImage(image=im2)

        #insertar imagen en la ventana
        lblInputImage1.configure(image=img)
        lblInputImage1.image = img
        lblInputImage2.configure(image=img2)
        lblInputImage2.image = img2

        #Insertar texto correspondiente a la imagen        
        lblInfo1 = Label(root, text="IMAGEN ORIGINAL")
        lblInfo2 = Label(root, text="IMAGEN ANALIZADA")
        lblInfo3.config(text=f"Contador: {len(contornos)}")
        lblInfo1.grid(column=0,row=1,padx=5,pady=5)
        lblInfo2.grid(column=1,row=1,padx=5,pady=5)

image = None

root = Tk()
root.geometry('1000x500+50+50')
root.title("Contador de malvas")

lblInputImage1 = Label(root)
lblInputImage1.grid(column=0,row=2)
lblInputImage2 = Label(root)
lblInputImage2.grid(column=1,row=2)
lblInfo3 = Label(root)
lblInfo3.grid(column=1, row=3)

btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0)


root.mainloop()

