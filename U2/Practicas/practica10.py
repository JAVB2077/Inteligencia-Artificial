import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivate(x):
    return x * (1 - x)

def imprimir_matriz(vector_plano, titulo):
    print(f"\n--- {titulo} ---")
    matriz = vector_plano.reshape((6, 8))
    for fila in matriz:
        print(" ".join(['■' if p == 1 else '.' for p in fila])) #219
    print("--------------------")

A_ideal = np.array([
    0,0,1,1,1,1,0,0,
    0,1,0,0,0,0,1,0,
    0,1,1,1,1,1,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0
])

E_ideal = np.array([
    0,1,1,1,1,1,1,0,
    0,1,0,0,0,0,0,0,
    0,1,1,1,1,1,0,0,
    0,1,0,0,0,0,0,0,
    0,1,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0
])

I_ideal = np.array([
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0
])

O_ideal = np.array([
    0,0,1,1,1,1,0,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,0,1,1,1,1,0,0
])

U_ideal = np.array([
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,0,1,1,1,1,0,0
])

N1_ideal = np.array([
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0
])

N2_ideal = np.array([
    0,0,1,1,1,1,0,0,
    0,1,0,0,0,0,1,0,
    0,0,0,0,0,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,0,0,0,0,0,
    0,1,1,1,1,1,1,0
])

N3_ideal = np.array([
    0,1,1,1,1,1,0,0,
    0,0,0,0,0,0,1,0,
    0,0,0,1,1,1,0,0,
    0,0,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,0,1,1,1,1,0,0
])

X_entrenamiento = np.array([A_ideal, E_ideal, I_ideal, O_ideal, U_ideal, N1_ideal, N2_ideal, N3_ideal])

Y_entrenamiento = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0], # A
    [0, 1, 0, 0, 0, 0, 0, 0], # E
    [0, 0, 1, 0, 0, 0, 0, 0], # I
    [0, 0, 0, 1, 0, 0, 0, 0], # O
    [0, 0, 0, 0, 1, 0, 0, 0], # U
    [0, 0, 0, 0, 0, 1, 0, 0], # 1
    [0, 0, 0, 0, 0, 0, 1, 0], # 2
    [0, 0, 0, 0, 0, 0, 0, 1]  # 3
])

clases_nombres = ['A', 'E', 'I', 'O', 'U', '1', '2', '3']

np.random.seed(42)
n_entradas = 48 # 6 filas x 8 columnas
n_salidas = 8  # 8 clases distintas

pesos = 2 * np.random.random((n_entradas, n_salidas)) - 1
sesgos = 2 * np.random.random((1, n_salidas)) - 1

tasa_aprendizaje = 0.5
epocas = 2000

print(" Entrenando la Red Neuronal ")
for epoca in range(epocas):
    # Propagation
    z = np.dot(X_entrenamiento, pesos) + sesgos
    salida = sigmoid(z)

    # Backpropagation
    error = Y_entrenamiento - salida
    ajustes = error * sigmoid_derivate(salida)

    pesos += np.dot(X_entrenamiento.T, ajustes) * tasa_aprendizaje
    sesgos += np.sum(ajustes, axis=0, keepdims=True) * tasa_aprendizaje

print(" ¡Entrenamiento completado!\n")

def reconocer_matriz(matriz_usuario):
    vector = np.array(matriz_usuario).flatten()
    if len(vector) != 48:
        print(f"Error: La matriz debe tener exactamente 48 elementos (6x8).")
        return

    imprimir_matriz(vector, "Matriz proporcionada por el usuario")

    z = np.dot(vector, pesos) + sesgos
    predicciones = sigmoid(z)[0]

    indice_ganador = np.argmax(predicciones)
    confianza = predicciones[indice_ganador] * 100

    print("Resultados de activación por neurona:")
    for i in range(n_salidas):
        print(f" Neurona [{clases_nombres[i]}]: {predicciones[i]*100:>5.1f}%")

    print(f"\n LA RED CONCLUYE QUE ES UN(A): '{clases_nombres[indice_ganador]}'")
    print(f" Confianza: {confianza:.2f}%")

matriz_prueba_A1 = [
    0,0,1,1,1,1,0,0,
    0,1,0,0,0,1,1,0,
    0,1,1,1,1,1,1,0,
    0,1,0,0,0,1,1,0,
    0,1,0,0,0,1,1,0,
    0,1,0,0,0,1,1,0
]
matriz_prueba_A2 = [
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,
    0,1,0,0,0,1,1,0,
    0,1,1,1,1,1,1,0,
    0,1,0,0,0,1,1,0
]
matriz_prueba_A3 = [
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0,1,0,1,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0,1,0,1,0,0,0,0
]
#E distorcionada para probar
matriz_prueba_E1 = [
    0,1,1,1,1,1,1,0,
    0,1,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,
    0,1,0,0,0,0,0,0,
    0,1,1,1,1,1,1,0,
    0,0,0,0,0,0,0,0
]
matriz_prueba_E2 = [
    1,1,1,1,1,1,1,1,
    1,1,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,
    1,1,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1
]
matriz_prueba_E3 = [
    0,0,0,0,0,0,0,0,
    0,0,1,1,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,1,1,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,1,1,0,0,0,0
]
matriz_prueba_I1 = [
    0,0,0,0,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,1,0,0,0,0,0
]
matriz_prueba_I2 = [
    0,0,0,0,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,1,1,1,0,0,0,0
]
matriz_prueba_I3 = [
    0,0,0,0,0,0,0,0,
    0,0,1,1,1,0,0,0,
    0,0,0,1,0,0,0,0,
    0,0,1,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
]
matriz_prueba_O1 = [
    [0, 0, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1, 1, 0, 0]
]
matriz_prueba_O2 = [
    0,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,0,
    0,1,1,0,0,1,1,0,
    0,1,1,0,0,1,1,0,
    0,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,0
]
matriz_prueba_O3 = [
    0,0,0,0,0,0,0,0,
    0,0,1,1,1,0,0,0,
    0,0,1,0,1,0,0,0,
    0,0,1,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
]
matriz_prueba_U1 = [
    0,1,0,1,0,0,0,0,
    0,1,0,1,0,0,0,0,
    0,1,0,1,0,0,0,0,
    0,1,0,1,0,0,0,0,
    0,1,0,1,0,0,0,0,
    0,0,1,1,0,0,0,0
]
matriz_prueba_U2 = [
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,0,1,1,1,1,0,0
]
matriz_prueba_U3 = [
    0,0,0,0,0,0,0,0,
    0,0,1,0,1,0,0,0,
    0,0,1,0,1,0,0,0,
    0,0,1,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
]

matriz_prueba_N2 = [
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0]
]

matriz_prueba_N1 = [
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0]
]


reconocer_matriz(matriz_prueba_U3)