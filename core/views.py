from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import requiere_rol
from .forms import PrestamoNotebookForm
from .models import PrestamoNotebook
from .services import evaluar_prestamo


@login_required
def prestamo_lista(request):
    prestamos = PrestamoNotebook.objects.filter(
        eliminado=False
    ).order_by("-creado_en")

    return render(
        request,
        "core/resumen.html",
        {"prestamos": prestamos},
    )


@requiere_rol("admin", "normal")
def prestamo_crear(request):
    if request.method == "POST":
        form = PrestamoNotebookForm(request.POST)

        if form.is_valid():
            prestamo = form.save(commit=False)

            prestamo.estado, prestamo.motivo = evaluar_prestamo(
                prestamo.edad,
                prestamo.cupos_disponibles,
            )

            prestamo.save()

            return redirect("prestamo_lista")

    else:
        form = PrestamoNotebookForm()

    return render(
        request,
        "core/prestamo_form.html",
        {"form": form},
    )


@requiere_rol("admin")
def prestamo_editar(request, pk):
    prestamo = get_object_or_404(
        PrestamoNotebook,
        pk=pk,
        eliminado=False,
    )

    if request.method == "POST":
        form = PrestamoNotebookForm(
            request.POST,
            instance=prestamo,
        )

        if form.is_valid():
            prestamo = form.save(commit=False)

            prestamo.estado, prestamo.motivo = evaluar_prestamo(
                prestamo.edad,
                prestamo.cupos_disponibles,
            )

            prestamo.save()

            return redirect("prestamo_lista")

    else:
        form = PrestamoNotebookForm(
            instance=prestamo,
        )

    return render(
        request,
        "core/prestamo_form.html",
        {
            "form": form,
            "es_edicion": True,
        },
    )


@requiere_rol("admin")
def prestamo_eliminar(request, pk):
    prestamo = get_object_or_404(
        PrestamoNotebook,
        pk=pk,
        eliminado=False,
    )

    if request.method == "POST":
        prestamo.soft_delete()
        return redirect("prestamo_lista")

    return render(
        request,
        "core/prestamo_confirmar_eliminacion.html",
        {"prestamo": prestamo},
    )
