import cv2

captura = cv2.VideoCapture(0)

if not captura.isOpened():
    print("Error al acceder a la camara")
    exit()

while True:
    ret, imagen = captura.read()

    if not ret:
        print("Error al leer el frame")
        break

    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Video en Escala de Grises', imagen_gris)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()