import tkinter as tk
from tkinter import messagebox
import requests

# ---------------- CONFIGURACIÓN ----------------
# URL del endpoint de la API para predicciones
API_URL = "http://127.0.0.1:8000/predecir"

# Matriz de estado: 48 valores (0 = apagado, 1 = activado)
# Corresponde a una grilla de 6 filas x 8 columnas
estado = [0] * 48
botones = []  # Lista para almacenar las referencias de los botones

# ---------------- FUNCIONES ----------------

def toggle(index):
    estado[index] = 1 if estado[index] == 0 else 0

    if estado[index] == 1:
        botones[index].config(bg="black")
    else:
        botones[index].config(bg="gray")


def predecir():
    # Verificar que al menos un botón esté seleccionado
    if sum(estado) == 0:
        messagebox.showwarning("Advertencia", "Selecciona al menos un patrón antes de predecir")
        return

    # Preparar los datos para enviar a la API
    datos = {
        "datos": estado
    }

    try:
        # Realizar la solicitud POST a la API
        respuesta = requests.post(API_URL, json=datos)

        # Si la respuesta es exitosa (código 200)
        if respuesta.status_code == 200:
            # Extraer la predicción de la respuesta JSON
            resultado = respuesta.json()
            prediccion = resultado["prediccion_final"]

            # Actualizar la etiqueta con el resultado
            label_resultado.config(text=f"Resultado: {prediccion}")

        else:
            # Error en la respuesta de la API
            messagebox.showerror("Error", "Error en la API")

    except:
        # Error de conexión con la API
        messagebox.showerror("Error", "No se pudo conectar a la API")


def limpiar():
    global estado
    estado = [0] * 48  # Reiniciar todos los valores a 0

    # Restaurar el color gris de todos los botones
    for btn in botones:
        btn.config(bg="gray")

    # Limpiar el texto del resultado
    label_resultado.config(text="Resultado: -")


# ---------------- INTERFAZ GRÁFICA ----------------

# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Reconocimiento de Patrones")
ventana.geometry("550x520")
ventana.config(bg="#f4f4f4")

# ----- Título de la aplicación -----
titulo = tk.Label(
    ventana,
    text="Reconocimiento de Patrones",
    font=("Arial", 14, "bold"),
    bg="#f4f4f4"
)
titulo.pack(pady=10)

# ----- Contenedor para la matriz de botones -----
frame_matriz = tk.Frame(ventana, bg="#f4f4f4")
frame_matriz.pack()

# ----- Generación de la matriz de botones (6x8) -----
filas = 6
columnas = 8

for i in range(filas):
    for j in range(columnas):
        # Calcular el índice lineal del botón (0 a 47)
        index = i * columnas + j

        # Crear cada botón con estado inicial apagado (gris)
        btn = tk.Button(
            frame_matriz,
            width=4,
            height=2,
            bg="gray",
            command=lambda idx=index: toggle(idx)
        )

        # Posicionar el botón en la cuadrícula
        btn.grid(row=i, column=j, padx=2, pady=2)
        botones.append(btn)

# ----- Etiqueta para mostrar el resultado -----
label_resultado = tk.Label(
    ventana,
    text="Resultado: -",
    font=("Arial", 14, "bold"),
    bg="#f4f4f4"
)
label_resultado.pack(pady=15)

# ----- Botón para ejecutar la predicción -----
btn_predecir = tk.Button(
    ventana,
    text="Predecir",
    font=("Arial", 12),
    width=20,
    command=predecir,
    bg="#4CAF50",
    fg="white"
)
btn_predecir.pack(pady=5)

# ----- Botón para limpiar la selección -----
btn_limpiar = tk.Button(
    ventana,
    text="Limpiar",
    font=("Arial", 12),
    width=20,
    command=limpiar
)
btn_limpiar.pack(pady=5)

# ---------------- INICIAR APLICACIÓN ----------------
# Iniciar el bucle principal de Tkinter
ventana.mainloop()
