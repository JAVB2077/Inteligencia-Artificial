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
    cv2.imshow("Captura de video", imagen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()