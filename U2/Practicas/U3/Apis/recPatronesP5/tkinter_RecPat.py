import tkinter as tk
from tkinter import messagebox
import requests

# URL de tu API
API_URL = "http://127.0.0.1:8000/predecir"

# Estado de la matriz (48 valores)
estado = [0] * 48
botones = []

# ---------------- FUNCIONES ----------------

def toggle(index):
    """Cambia el estado del botón"""
    estado[index] = 1 if estado[index] == 0 else 0

    if estado[index] == 1:
        botones[index].config(bg="black")
    else:
        botones[index].config(bg="white")


def predecir():
    """Envía datos a la API"""
    datos = {
        "datos": estado
    }

    try:
        respuesta = requests.post(API_URL, json=datos)

        if respuesta.status_code == 200:
            resultado = respuesta.json()
            prediccion = resultado["prediccion_final"]

            label_resultado.config(text=f"Resultado: {prediccion}")

        else:
            messagebox.showerror("Error", "Error en la API")

    except:
        messagebox.showerror("Error", "No se pudo conectar a la API")


def limpiar():
    """Reinicia todo"""
    global estado
    estado = [0] * 48

    for btn in botones:
        btn.config(bg="white")

    label_resultado.config(text="Resultado: -")


# ---------------- INTERFAZ ----------------

ventana = tk.Tk()
ventana.title("Reconocimiento de Patrones")
ventana.geometry("400x500")
ventana.config(bg="#f4f4f4")

# Título
titulo = tk.Label(
    ventana,
    text="Reconocimiento de Patrones",
    font=("Arial", 14, "bold"),
    bg="#f4f4f4"
)
titulo.pack(pady=10)

# Frame de la matriz
frame_matriz = tk.Frame(ventana, bg="#f4f4f4")
frame_matriz.pack()

# Crear botones 6x8
filas = 6
columnas = 8

for i in range(filas):
    for j in range(columnas):
        index = i * columnas + j

        btn = tk.Button(
            frame_matriz,
            width=4,
            height=2,
            bg="white",
            command=lambda idx=index: toggle(idx)
        )

        btn.grid(row=i, column=j, padx=2, pady=2)
        botones.append(btn)

# Resultado
label_resultado = tk.Label(
    ventana,
    text="Resultado: -",
    font=("Arial", 14, "bold"),
    bg="#f4f4f4"
)
label_resultado.pack(pady=15)

# Botón predecir
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

# Botón limpiar
btn_limpiar = tk.Button(
    ventana,
    text="Limpiar",
    font=("Arial", 12),
    width=20,
    command=limpiar
)
btn_limpiar.pack(pady=5)

# Ejecutar app
ventana.mainloop()