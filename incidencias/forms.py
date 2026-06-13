from django import forms
from .models import Incidencia


class IncidenciaForm(forms.ModelForm):

    class Meta:
        model = Incidencia

        fields = [
            "titulo",
            "descripcion",
            "prioridad",
        ]

        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
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
                
class ResolverIncidenciaForm(forms.Form):

    solucion = forms.CharField(
        label="Solución aplicada",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "form-control"
            }
        )
    )