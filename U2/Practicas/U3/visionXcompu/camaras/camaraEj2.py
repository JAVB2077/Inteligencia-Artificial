import cv2

captura = cv2.VideoCapture(0)

if not captura.isOpened():
    print("No se pudo abrir la cámara")
    exit()

while True:
    ret, imagen = captura.read()
    if not ret:
        print("No se pudo capturar la imagen")
        break

    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    bordes = cv2.Canny(imagen_gris, 50, 150)

    cv2.imshow("Deteccion de bordes Canny", bordes)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()