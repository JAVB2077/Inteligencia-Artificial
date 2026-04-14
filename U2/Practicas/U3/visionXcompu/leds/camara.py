import cv2
import mediapipe as mp
import requests

# Configuración
ESP32_IP = "http://192.168.1.78." # Cambia por tu IP
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# IDs de los puntos de las puntas de los dedos (MediaPipe)
tip_ids = [4, 8, 12, 16, 20]
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1) # Efecto espejo
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    dedos_estado = ["0", "0", "0", "0", "0"] # Estado inicial (apagados)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Lógica para el Pulgar (comparación horizontal)
            if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x:
                dedos_estado[0] = "1"
            
            # Lógica para los otros 4 dedos (comparación vertical)
            for i in range(1, 5):
                if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
                    dedos_estado[i] = "1"

        # Enviar estado al ESP32
        estado_str = "".join(dedos_estado)
        try:
            requests.get(f"{ESP32_IP}/SET?state={estado_str}", timeout=0.1)
        except:
            pass

    cv2.imshow("Control de LEDs por Gestos", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()