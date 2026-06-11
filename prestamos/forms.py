from django import forms
from .models import Prestamo, LineaPrestamo
from inventario.models import Material

class PrestamoForm(forms.ModelForm):

    class Meta:
        model = Prestamo

        fields = [
            "usuario_receptor",
            "profesor_responsable",
            "fecha_prevista_devolucion",
            "observaciones",
        ]

        widgets = {
            "fecha_prevista_devolucion": forms.DateInput(
                attrs={"type": "date"}
            ),
            "observaciones": forms.Textarea(
                attrs={"rows": 3}
            ),
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


class LineaPrestamoForm(forms.ModelForm):

    class Meta:
        model = LineaPrestamo

        fields = [
            "material",
            "cantidad",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["material"].queryset = Material.objects.filter(
            estado="disponible"
        )

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

    def clean_material(self):
        material = self.cleaned_data["material"]

        if material.estado != "disponible":
            raise forms.ValidationError(
                "Este material no está disponible para préstamo."
            )

        return material