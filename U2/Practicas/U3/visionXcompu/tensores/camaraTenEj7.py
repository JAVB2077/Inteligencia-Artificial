#hands2
import cv2
import mediapipe as mp

mp_manos = mp.solutions.hands
manos = mp_manos.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_dibujo = mp.solutions.drawing_utils

captura = cv2.VideoCapture(0)

# Puntos de las puntas de los dedos: Pulgar, Índice, Medio, Anular y Meñique
puntas = [4, 8, 12, 16, 20]

while True:
    ret, imagen = captura.read()
    if not ret:
        break

    imagen = cv2.flip(imagen, 1)
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    resultados = manos.process(imagen_rgb)

    if resultados.multi_hand_landmarks:
        for puntos_mano in resultados.multi_hand_landmarks:
            mp_dibujo.draw_landmarks(imagen, puntos_mano, mp_manos.HAND_CONNECTIONS)
            
            dedos_levantados = []
            lista_puntos = []

            # Extraer las coordenadas de cada punto
            for id, punto in enumerate(puntos_mano.landmark):
                alto, ancho, _ = imagen.shape
                cx, cy = int(punto.x * ancho), int(punto.y * alto)
                lista_puntos.append([id, cx, cy])

            if len(lista_puntos) != 0:
                # Lógica para el Pulgar (se compara en el eje X para ver si está extendido)
                if lista_puntos[puntas[0]][1] > lista_puntos[puntas[0] - 1][1]:
                    dedos_levantados.append(1)
                else:
                    dedos_levantados.append(0)

                # Lógica para los otros 4 dedos (se compara el eje Y)
                for id in range(1, 5):
                    if lista_puntos[puntas[id]][2] < lista_puntos[puntas[id] - 2][2]:
                        dedos_levantados.append(1)
                    else:
                        dedos_levantados.append(0)

                total_dedos = dedos_levantados.count(1)

                # Mostrar el conteo en pantalla
                cv2.putText(imagen, f'Dedos: {total_dedos}', (40, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Contador de Dedos", imagen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()