class Perceptron:
    def __init__(self, tasa_aprendizaje=0.1, epocas=10):
        # Inicializamos los pesos y el sesgo en 0
        self.w1 = 0.0
        self.w2 = 0.0
        self.b = 0.0
        self.tasa_aprendizaje = tasa_aprendizaje
        self.epocas = epocas

    def funcion_activacion(self, z):
        # Función Escalón simple: retorna 1 si z es positivo, 0 si es negativo
        return 1 if z >= 0 else 0

    def predecir(self, x1, x2):
        # 1. Calculamos la suma ponderada: (Entradas * Pesos) + Sesgo
        z = (self.w1 * x1) + (self.w2 * x2) + self.b
        # 2. Pasamos el resultado por la función de activación
        return self.funcion_activacion(z)

    def entrenar(self, datos_X, datos_Y):
        print("Iniciando entrenamiento del Perceptrón...\n")

        for epoca in range(self.epocas):
            errores_epoca = 0

            # Recorremos cada ejemplo de nuestro set de datos
            for i in range(len(datos_X)):
                x1, x2 = datos_X[i]
                salida_esperada = datos_Y[i]

                # La neurona intenta predecir
                prediccion = self.predecir(x1, x2)

                # Calculamos el error (Esperado - Predicción)
                error = salida_esperada - prediccion

                # Si hay error, ajustamos (pesos y sesgo)
                if error != 0:
                    self.w1 += self.tasa_aprendizaje * error * x1
                    self.w2 += self.tasa_aprendizaje * error * x2
                    self.b += self.tasa_aprendizaje * error
                    errores_epoca += 1

            print(f"Época {epoca + 1}/{self.epocas} - Errores cometidos: {errores_epoca}")
            print(f"    Pesos actuales -> w1: {self.w1:.2f}, w2: {self.w2:.2f}, b: {self.b:.2f}")

            # Si en una época completa no cometió errores
            if errores_epoca == 0:
                print("\n¡El perceptrón ha convergido (aprendió el patrón)!")
                break

if __name__ == "__main__":
    # --- DATOS DE ENTRENAMIENTO (Compuerta AND) ---
    X = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]
    
    # Salidas esperadas
    Y = [0, 0, 0, 1]

    # perceptrón con una tasa de aprendizaje de 0.1 y máximo 10 intentos
    mi_neurona = Perceptron(tasa_aprendizaje=0.1, epocas=10)

    # Entrenamiento
    mi_neurona.entrenar(X, Y)

    print("Probando las entradas para ver si aprendió correctamente:")
    for i in range(len(X)):
        x1, x2 = X[i]
        resultado = mi_neurona.predecir(x1, x2)
        print(f"Entrada: Movimiento={x1}, Máquina={x2} -> Alarma (Predicción): {resultado}")