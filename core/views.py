import json
from pathlib import Path

from django.shortcuts import render


def resumen(request):
    ruta_datos = Path(__file__).resolve().parent.parent / "datos.json"

    try:
        with open(ruta_datos, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)
    except FileNotFoundError:
        registros = []

    return render(request, "core/resumen.html", {"registros": registros})
