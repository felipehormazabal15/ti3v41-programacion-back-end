from rest_framework.permissions import BasePermission, SAFE_METHODS


class PrestamoNotebookPermission(BasePermission):
    """
    Permisos para la API de préstamos:

    - Usuarios autenticados pueden consultar.
    - Usuarios de los grupos admin y normal pueden crear.
    - Solo usuarios del grupo admin pueden modificar o eliminar.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            return user.groups.filter(name__in=["admin", "normal"]).exists()

        if request.method in ("PUT", "PATCH", "DELETE"):
            return user.groups.filter(name="admin").exists()

        return False
