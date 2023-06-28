import cv2
import imutils #libreria para escalar imagenes "pip install imutils"

imagen = cv2.imread("./malva2.jpg") #abrir imagen
imagen = imutils.resize(imagen, width=1200) #re escalar imagen

grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY) #cambia a escala de grises
bordes = cv2.Canny(grises, 150, 400) #DETECCION DE BORDES la funcion pide (imagen, umbral bajo, umbral alto)
#los bordes con valores mas alla del umbral alto, se dibujaran
#mientras que los bordes con valores mas bajos, solo se dibujaran si estan conectados a bordes ya encontrados en el umbral alto

contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #encontrar contornos en la imagen "bordes"

cv2.drawContours(imagen, contornos, -1, (0, 255, 0), 2) #dibujar contornos, en imagen

print("Numero de contornos obtenidos: ", len(contornos)) #imprimir numero de contornos encontrados

cv2.imshow("ORIGINAL", imagen) #mostrar imagen
cv2.waitKey(0) #espera para presionar una tecla y cerrar ventana
cv2.destroyAllWindows() #cierra todas las ventanas