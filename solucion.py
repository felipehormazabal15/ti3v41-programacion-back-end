import json
from tabulate import tabulate

try:
    with open("datos.json", "r", encoding="utf-8") as archivo:
        registros = json.load(archivo)
except FileNotFoundError:
    registros = []

nombre = input("Nombre: ")
edad = int(input("Edad: "))
cupos = int(input("Cantidad de notebooks disponibles: "))

if cupos < 0:
    estado = "Dato inválido"
    motivo = "La cantidad de notebooks no puede ser negativa."

elif edad < 18:
    estado = "Rechazado"
    motivo = "La persona es menor de 18 años."

elif cupos == 0:
    estado = "Rechazado"
    motivo = "No hay notebooks disponibles."

elif edad >= 18 and cupos > 0:
    estado = "Aceptado"
    motivo = "La persona cumple la edad requerida y hay notebooks disponibles."

registro = {
    "nombre": nombre,
    "edad": edad,
    "cupos": cupos,
    "estado": estado,
    "motivo": motivo
}

registros.append(registro)

with open("datos.json", "w", encoding="utf-8") as archivo:
    json.dump(registros, archivo, indent=2, ensure_ascii=False)

print("\n===== RESULTADO =====")
print(f"Nombre: {nombre}")
print(f"Estado: {estado}")
print(f"Motivo: {motivo}")

print("\n===== REGISTROS =====")
tabla = []

for registro in registros:
    tabla.append([
        registro["nombre"],
        registro["edad"],
        registro["cupos"],
        registro["estado"],
        registro["motivo"]
    ])

print(tabulate(
    tabla,
    headers=["nombre", "edad", "cupos", "estado", "motivo"],
    tablefmt="grid"
))
