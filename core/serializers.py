from rest_framework import serializers

from .models import PrestamoNotebook


class PrestamoNotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestamoNotebook
        fields = (
            "id",
            "nombre",
            "edad",
            "cupos_disponibles",
            "estado",
            "motivo",
            "creado_en",
            "eliminado",
            "fecha_eliminacion",
        )
        read_only_fields = (
            "id",
            "estado",
            "motivo",
            "creado_en",
            "eliminado",
            "fecha_eliminacion",
        )

    def validate_nombre(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre no puede estar vacío."
            )
        return value.strip()

    def validate_cupos_disponibles(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "La cantidad de notebooks no puede ser negativa."
            )
        return value
