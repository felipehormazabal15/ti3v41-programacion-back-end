from django.contrib import admin

from .models import PrestamoNotebook


@admin.register(PrestamoNotebook)
class PrestamoNotebookAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "edad",
        "cupos_disponibles",
        "estado",
        "eliminado",
        "creado_en",
        "fecha_eliminacion",
    )

    list_filter = (
        "estado",
        "eliminado",
        "creado_en",
    )

    search_fields = ("nombre",)

    ordering = ("-creado_en",)

    readonly_fields = (
        "creado_en",
        "fecha_eliminacion",
    )