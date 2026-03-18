import tkinter as tk
from tkinter import messagebox
import requests

# URL base de tu API local (Asegúrate de que el puerto sea el correcto, usualmente 8000)
API_URL = "http://127.0.0.1:8000"

def calcular(endpoint):
    # Obtener los valores de las cajas de texto
    valor_a = caja_a.get()
    valor_b = caja_b.get()
    
    # Validar que no estén vacíos y sean números
    try:
        num1 = float(valor_a)
        num2 = float(valor_b)
    except ValueError:
        messagebox.showwarning("Atención", "Por favor, ingresa solo números en las cajas A y B.")
        return

    # Estructurar los datos como los espera FastAPI (Basado en tu clase 'Operacion')
    datos = {
        "numero1": num1,
        "numero2": num2
    }
    
    try:
        # Hacer la petición POST a la API
        respuesta = requests.post(f"{API_URL}/{endpoint}", json=datos)
        
        # Si la conexión es exitosa (Status 200)
        if respuesta.status_code == 200:
            resultado_json = respuesta.json()
            resultado_final = resultado_json["resultado_final"]
            
            # Mostrar el resultado en la última caja
            caja_resultado.config(state="normal") # Habilitar escritura temporalmente
            caja_resultado.delete(0, tk.END)
            caja_resultado.insert(0, str(resultado_final))
            caja_resultado.config(state="readonly") # Volver a modo solo lectura
        else:
            messagebox.showerror("Error", "Hubo un problema procesando la operación en la API.")
            
    except requests.exceptions.RequestException:
        messagebox.showerror("Error de conexión", "No se pudo conectar a la API. ¿Está corriendo el servidor?")

# --- Creación de la Interfaz  ---
ventana = tk.Tk()
ventana.title("Calculadora API")
ventana.geometry("300x450")
ventana.config(bg="#f4f7f6")

# Contenedor para la fila A
frame_a = tk.Frame(ventana, bg="#f4f7f6")
frame_a.pack(pady=15)
etiqueta_a = tk.Label(frame_a, text="A", font=("Arial", 16, "bold"), bg="#f4f7f6")
etiqueta_a.pack(side=tk.LEFT, padx=10)
caja_a = tk.Entry(frame_a, font=("Arial", 14), width=12, justify="center")
caja_a.pack(side=tk.LEFT)

# Contenedor para la fila B
frame_b = tk.Frame(ventana, bg="#f4f7f6")
frame_b.pack(pady=5)
etiqueta_b = tk.Label(frame_b, text="B", font=("Arial", 16, "bold"), bg="#f4f7f6")
etiqueta_b.pack(side=tk.LEFT, padx=10)
caja_b = tk.Entry(frame_b, font=("Arial", 14), width=12, justify="center")
caja_b.pack(side=tk.LEFT)

# Botones con sus respectivas funciones enviando el "endpoint" a usar
boton_sumar = tk.Button(ventana, text="Sumar", command=lambda: calcular("sumar"), font=("Arial", 12), width=15)
boton_sumar.pack(pady=10)

boton_restar = tk.Button(ventana, text="restar", command=lambda: calcular("restar"), font=("Arial", 12), width=15)
boton_restar.pack(pady=10)

boton_multiplicar = tk.Button(ventana, text="multiplicar", command=lambda: calcular("multiplicar"), font=("Arial", 12), width=15)
boton_multiplicar.pack(pady=10)

# Caja de resultado final (en modo solo lectura para que actúe como display)
caja_resultado = tk.Entry(ventana, font=("Arial", 14, "bold"), width=12, justify="center", state="readonly")
caja_resultado.pack(pady=30)

# Iniciar la aplicación
ventana.mainloop()