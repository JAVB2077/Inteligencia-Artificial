from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.neural_network import MLPClassifier

# --- 1. DATOS DE ENTRENAMIENTO ---
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
    0,0,0,0,1,0,0,0,
    0,0,0,1,0,0,0,0,
    0,0,1,1,1,1,1,0
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
Y_entrenamiento = np.array(['A','E','I','O','U','1','2','3'])

# --- 2. ENTRENAMIENTO DEL MODELO ---
print("Iniciando entrenamiento con Scikit-Learn...")
red_neuronal = MLPClassifier(
    hidden_layer_sizes=(24,),
    activation='relu',
    solver='adam',
    max_iter=1000,
    random_state=42
)
red_neuronal.fit(X_entrenamiento, Y_entrenamiento)
print(f"Entrenamiento completado en {red_neuronal.n_iter_} epocas.")
print(f"Error final (Loss): {red_neuronal.loss_:.4f}\n")


# --- 3. CONFIGURACIÓN DE LA API ---
app = FastAPI(
    title="API de Red Neuronal",
    description="API que recibe una matriz de 48 elementos y predice la letra o número.",
    version="1.0"
)

# --- 4. MODELOS DE DATOS (PYDANTIC) ---
class MatrizEntrada(BaseModel):
    # Esperamos una lista de 48 números (0s y 1s)
    datos: list[int]

class Operacion(BaseModel):
    numero1: float
    numero2: float


# --- 5. ENDPOINTS (RUTAS) ---

@app.get("/")
def ruta_raiz():
    return {"mensaje": "¡Hola! La API y la Red Neuronal están corriendo."}

#@app.post("/sumar")
#def sumar_numeros(datos: Operacion):
#    return {"resultado": datos.numero1 + datos.numero2}

# ¡NUEVO ENDPOINT PARA LA RED NEURONAL!
@app.post("/predecir")
def predecir_caracter(matriz: MatrizEntrada):
    # Validar que vengan exactamente 48 elementos (6x8)
    if len(matriz.datos) != 48:
        return {"error": f"La matriz debe tener 48 elementos. Se recibieron {len(matriz.datos)}."}
    
    # Convertir la lista a un array de numpy
    vector_plano = np.array(matriz.datos)
    
    # Hacer la predicción
    prediccion = red_neuronal.predict([vector_plano])
    probabilidades = red_neuronal.predict_proba([vector_plano])[0]
    clases = red_neuronal.classes_
    
    # Formatear el diccionario de confianza (probabilidades)
    analisis_confianza = {}
    for i in range(len(clases)):
        analisis_confianza[clases[i]] = f"{probabilidades[i]*100:.2f}%"

    return {
        
        "prediccion_final": prediccion[0],
        "confianza": analisis_confianza,
        "matriz_recibida": matriz.datos
    }