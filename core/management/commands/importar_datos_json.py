import json
from pathlib import Path

from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import PrestamoNotebook


class Command(BaseCommand):
    help = "Importa los préstamos históricos desde datos.json."

    campos_requeridos = {"nombre", "edad", "cupos", "estado", "motivo"}
    estados = {
        "Aceptado": PrestamoNotebook.Estado.ACEPTADO,
        "Rechazado": PrestamoNotebook.Estado.RECHAZADO,
        "Dato inválido": PrestamoNotebook.Estado.INVALIDO,
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Valida los registros sin insertarlos en la base de datos.",
        )

    def handle(self, *args, **options):
        registros = self.leer_registros()
        prestamos, errores = self.validar_registros(registros)

        if errores:
            for error in errores:
                self.stderr.write(self.style.ERROR(error))
            raise CommandError(
                f"La importación fue cancelada: se encontraron {len(errores)} errores."
            )

        cantidad = len(prestamos)
        if options["dry_run"]:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Validación correcta: se importarían {cantidad} registros."
                )
            )
            self.stdout.write("Modo dry-run: no se insertó ningún registro.")
            return

        existentes = PrestamoNotebook.objects.count()
        if existentes:
            raise CommandError(
                "La importación fue cancelada: PrestamoNotebook ya contiene "
                f"{existentes} registros. No se eliminaron ni modificaron datos existentes."
            )

        with transaction.atomic():
            for prestamo in prestamos:
                prestamo.save()

        self.stdout.write(
            self.style.SUCCESS(f"Importación completada: {cantidad} registros importados.")
        )

    def leer_registros(self):
        ruta_datos = Path(settings.BASE_DIR) / "datos.json"

        try:
            with ruta_datos.open("r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError as error:
            raise CommandError(f"No se encontró el archivo de datos: {ruta_datos}") from error
        except json.JSONDecodeError as error:
            raise CommandError(f"datos.json no contiene JSON válido: {error}") from error

        if not isinstance(registros, list):
            raise CommandError("datos.json debe contener una lista de registros.")

        return registros

    def validar_registros(self, registros):
        prestamos = []
        errores = []

        for indice, registro in enumerate(registros, start=1):
            try:
                prestamos.append(self.construir_prestamo(registro, indice))
            except ValueError as error:
                errores.append(str(error))

        return prestamos, errores

    def construir_prestamo(self, registro, indice):
        if not isinstance(registro, dict):
            raise ValueError(f"Registro {indice}: debe ser un objeto JSON.")

        claves = set(registro)
        faltantes = self.campos_requeridos - claves
        adicionales = claves - self.campos_requeridos
        if faltantes or adicionales:
            detalle = []
            if faltantes:
                detalle.append(f"faltan campos: {', '.join(sorted(faltantes))}")
            if adicionales:
                detalle.append(f"campos no permitidos: {', '.join(sorted(adicionales))}")
            raise ValueError(f"Registro {indice}: {'; '.join(detalle)}.")

        nombre = registro["nombre"]
        edad = registro["edad"]
        cupos = registro["cupos"]
        estado_json = registro["estado"]
        motivo = registro["motivo"]

        if not isinstance(nombre, str):
            raise ValueError(f"Registro {indice}: nombre debe ser texto.")
        if not isinstance(edad, int) or isinstance(edad, bool):
            raise ValueError(f"Registro {indice}: edad debe ser un entero.")
        if not isinstance(cupos, int) or isinstance(cupos, bool):
            raise ValueError(f"Registro {indice}: cupos debe ser un entero.")
        if not isinstance(estado_json, str) or estado_json not in self.estados:
            raise ValueError(f"Registro {indice}: estado no reconocido.")
        if not isinstance(motivo, str):
            raise ValueError(f"Registro {indice}: motivo debe ser texto.")

        prestamo = PrestamoNotebook(
            nombre=nombre,
            edad=edad,
            cupos_disponibles=cupos,
            estado=self.estados[estado_json],
            motivo=motivo,
        )

        try:
            prestamo.full_clean()
        except ValidationError as error:
            raise ValueError(f"Registro {indice}: datos no válidos: {error}") from error

        return prestamo
