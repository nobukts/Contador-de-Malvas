# Import required libraries
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np

def elegir_imagen():
    path_image = filedialog.askopenfilename(filetypes=[("image", ".jpg"),("image", ".jpeg"),("image",".png")])
    if len(path_image) > 0:
        global image
        image = cv2.imread(path_image)
        image = imutils.resize(image, height=500)
        imageToShow = imutils.resize(image, width=500)
        imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage1.configure(image=img)
        lblInputImage1.image = img
        lblInputImage2.configure(image=img)
        lblInputImage2.image = img

        lblInfo1 = Label(root, text="IMAGEN DE ENTRADA 1")
        lblInfo2 = Label(root, text="IMAGEN DE ENTRADA 2")
        lblInfo1.grid(column=0,row=1,padx=5,pady=5)
        lblInfo2.grid(column=1,row=1,padx=5,pady=5)


image = None
root = Tk()

lblInputImage1 = Label(root)
lblInputImage1.grid(column=0,row=2)
lblInputImage2 = Label(root)
lblInputImage2.grid(column=1,row=2)

btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0)


root.mainloop()

