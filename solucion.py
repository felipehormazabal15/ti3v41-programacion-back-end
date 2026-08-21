import json
from tabulate import tabulate

try:
    with open("datos.json", "r") as archivo:
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

else:
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

with open("datos.json", "w") as archivo:
    json.dump(registros, archivo, indent=2, ensure_ascii=False)

print()
print("===== RESULTADO =====")
print(f"Nombre: {nombre}")
print(f"Estado: {estado}")
print(f"Motivo: {motivo}")

print()
print("===== REGISTROS =====")
print(tabulate(registros, headers="keys", tablefmt="grid"))
