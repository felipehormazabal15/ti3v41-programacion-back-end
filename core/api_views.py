from rest_framework import viewsets

from .models import PrestamoNotebook
from .permissions import PrestamoNotebookPermission
from .serializers import PrestamoNotebookSerializer
from .services import evaluar_prestamo


class PrestamoNotebookViewSet(viewsets.ModelViewSet):
    serializer_class = PrestamoNotebookSerializer
    permission_classes = [PrestamoNotebookPermission]

    def get_queryset(self):
        return PrestamoNotebook.objects.filter(
            eliminado=False
        ).order_by("-creado_en")

    def perform_create(self, serializer):
        prestamo = serializer.save()
        prestamo.estado, prestamo.motivo = evaluar_prestamo(
            prestamo.edad,
            prestamo.cupos_disponibles,
        )
        prestamo.save(update_fields=["estado", "motivo"])

    def perform_update(self, serializer):
        prestamo = serializer.save()
        prestamo.estado, prestamo.motivo = evaluar_prestamo(
            prestamo.edad,
            prestamo.cupos_disponibles,
        )
        prestamo.save(update_fields=["estado", "motivo"])

    def perform_destroy(self, instance):
        instance.soft_delete()
