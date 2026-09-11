from django.urls import path

from .views import prestamo_crear, prestamo_editar, prestamo_eliminar, prestamo_lista

urlpatterns = [
    path("", prestamo_lista, name="prestamo_lista"),
    path("prestamos/nuevo/", prestamo_crear, name="prestamo_crear"),
    path("prestamos/<int:pk>/editar/", prestamo_editar, name="prestamo_editar"),
    path("prestamos/<int:pk>/eliminar/", prestamo_eliminar, name="prestamo_eliminar"),
]
