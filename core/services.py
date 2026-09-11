from .models import PrestamoNotebook


def evaluar_prestamo(edad: int, cupos_disponibles: int) -> tuple[str, str]:
    """Evalúa una solicitud de préstamo según la edad y los cupos disponibles."""
    if cupos_disponibles < 0:
        return PrestamoNotebook.Estado.INVALIDO, "Dato inválido"

    if edad < 18:
        return (
            PrestamoNotebook.Estado.RECHAZADO,
            "La persona es menor de 18 años.",
        )

    if cupos_disponibles == 0:
        return (
            PrestamoNotebook.Estado.RECHAZADO,
            "No hay notebooks disponibles.",
        )

    return (
        PrestamoNotebook.Estado.ACEPTADO,
        "La persona cumple la edad requerida y hay notebooks disponibles.",
    )
