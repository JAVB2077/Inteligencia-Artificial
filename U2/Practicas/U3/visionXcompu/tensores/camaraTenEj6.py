#Hands1.py
import cv2
import mediapipe as mp

mp_manos = mp.solutions.hands
manos = mp_manos.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_dibujo = mp.solutions.drawing_utils

captura = cv2.VideoCapture(0)

while True:
    ret, imagen = captura.read()

    if not ret:
        break

    imagen = cv2.flip(imagen, 1)
    # Convertir de BGR a RGB
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    resultados = manos.process(imagen_rgb)

    # Revisar si la red neuronal encontró alguna mano
    if resultados.multi_hand_landmarks:
        for puntos_mano in resultados.multi_hand_landmarks:
            # Dibujar los 21 puntos y sus conexiones
            mp_dibujo.draw_landmarks(imagen, puntos_mano, mp_manos.HAND_CONNECTIONS)

    cv2.imshow("Control Gestual - MediaPipe", imagen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()