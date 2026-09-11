from django import forms

from .models import PrestamoNotebook


class PrestamoNotebookForm(forms.ModelForm):
    class Meta:
        model = PrestamoNotebook
        fields = ("nombre", "edad", "cupos_disponibles")
