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

    contornos, _ = cv2.findContours(mascara,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contorno in contornos:
        area = cv2.contourArea(contorno)

        if area > 1000:
            momentos = cv2.moments(contorno)

            if momentos['m00'] > 0:
                cx = int(momentos['m10']/momentos['m00'])
                cy = int(momentos['m01']/momentos['m00'])

                cv2.drawContours(imagen,[contorno],-1,(0,255,0),2)
                print(f"Objeto detectado en X: {cx} Y: {cy}")

    cv2.imshow('Seguimiento de Objeto Verde',imagen)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   
captura.release()
cv2.destroyAllWindows()