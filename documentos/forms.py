from django import forms
from .models import Documento, Fotografia


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


class FotografiaForm(forms.ModelForm):

    class Meta:
        model = Fotografia

        fields = [
            "titulo",
            "imagen",
            "descripcion",
        ]

        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

    def clean_imagen(self):
        imagen = self.cleaned_data["imagen"]

        if imagen.size == 0:
            raise forms.ValidationError("La imagen no puede estar vacía.")

        if imagen.content_type and not imagen.content_type.startswith("image/"):
            raise forms.ValidationError("El archivo debe ser una imagen.")

        return imagen
