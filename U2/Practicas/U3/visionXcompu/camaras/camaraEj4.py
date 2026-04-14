import cv2
import numpy as np

captura = cv2.VideoCapture(0)

if not captura.isOpened():
    print("Error al acceder a la camara")
    exit()

verde_bajo=np.array([35,40,40],np.uint8)
verde_alto=np.array([85,255,255],np.uint8)

while True:
    ret, imagen = captura.read()

    if not ret:
        print("Error al leer el frame")
        break

    imagen_hsv = cv2.cvtColor(imagen,cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(imagen_hsv,verde_bajo,verde_alto)

    cv2.imshow('Video Origuinal',imagen)
    cv2.imshow('Mascara de Color Verde',mascara)

    if cv2.waitKey(1) & 0xFF  == ord ('q'):
        break

captura.release()
cv2.destroyAllWindows()

#mediapipe,