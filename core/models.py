from django.db import models
from django.utils import timezone


class PrestamoNotebook(models.Model):
    """Registro de una solicitud y su evaluación de préstamo."""

    class Estado(models.TextChoices):
        ACEPTADO = "ACEPTADO", "Aceptado"
        RECHAZADO = "RECHAZADO", "Rechazado"
        INVALIDO = "INVALIDO", "Dato inválido"

    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    cupos_disponibles = models.IntegerField()
    estado = models.CharField(max_length=10, choices=Estado.choices)
    motivo = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "préstamo de notebook"
        verbose_name_plural = "préstamos de notebooks"

    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"

    def soft_delete(self):
        """Marca el préstamo como eliminado sin borrarlo de la base de datos."""
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save(update_fields=["eliminado", "fecha_eliminacion"])