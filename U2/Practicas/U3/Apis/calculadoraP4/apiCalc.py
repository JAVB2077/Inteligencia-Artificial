from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Mi API para calculadora",
    description="API de prueba para aprender a levantar servicios web y usar tkinter",
    version="1.0"
)

class Operacion(BaseModel):
    numero1: float
    numero2: float

# Método GET simple
@app.get("/")
def ruta_raiz():
    return {
        "mensaje": "¡Hola, mundo!",
        "estado": "El servidor está corriendo."
    }

# GET con variables en la URL
# Si entra a /saludo/Emm, la API leerá "Emm"
@app.get("/saludo/{nombre}")
def saludar_usuario(nombre: str):
    return {
        "mensaje": f"¡Hola, {nombre}! Bienvenido a la clase"
    }

# POST sumar
@app.post("/sumar")
def sumar_numeros(datos: Operacion):
    resultado = datos.numero1 + datos.numero2
    return {
        "operacion": "suma",
        "numeros_recibidos": [datos.numero1, datos.numero2],
        "resultado_final": resultado
    }
#  POST para restar
@app.post("/restar")
def restar_numeros(datos: Operacion):
    resultado = datos.numero1 - datos.numero2
    return {
        "operacion": "resta",
        "resultado_final": resultado
    }

# POST para multiplicar
@app.post("/multiplicar")
def multiplicar_numeros(datos: Operacion):
    resultado = datos.numero1 * datos.numero2
    return {
        "operacion": "multiplicacion",
        "resultado_final": resultado
    }