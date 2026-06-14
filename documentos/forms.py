from django import forms
from .models import Documento


class DocumentoForm(forms.ModelForm):

    class Meta:
        model = Documento

        fields = [
            "nombre",
            "descripcion",
            "archivo",
            "tipo_documento",
        ]

        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

        for nombre, campo in self.fields.items():
            if isinstance(
                campo.widget,
                (
                    forms.Select,
                    forms.SelectMultiple
                )
            ):
                campo.widget.attrs["class"] = "form-select"

    def clean_archivo(self):
        archivo = self.cleaned_data["archivo"]

        if archivo.size == 0:
            raise forms.ValidationError("El archivo no puede estar vacío.")

        return archivo
