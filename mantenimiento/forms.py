from django import forms

from .models import Mantenimiento, PlanMantenimiento


class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = [
            "tipo",
            "fecha",
            "descripcion",
            "resultado",
            "coste",
            "proxima_revision",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "proxima_revision": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["coste"].widget.attrs["min"] = "0"
        self.fields["coste"].widget.attrs["step"] = "0.01"

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

        for campo in self.fields.values():
            if isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"


class PlanMantenimientoForm(forms.ModelForm):
    class Meta:
        model = PlanMantenimiento
        fields = [
            "nombre",
            "tipo",
            "descripcion",
            "frecuencia_dias",
            "fecha_inicio",
            "proxima_revision",
            "activo",
            "observaciones",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "proxima_revision": forms.DateInput(attrs={"type": "date"}),
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["frecuencia_dias"].widget.attrs["min"] = "1"
        self.fields["frecuencia_dias"].widget.attrs["step"] = "1"

        for nombre, campo in self.fields.items():
            if nombre == "activo":
                campo.widget.attrs["class"] = "form-check-input"
            elif isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"
            else:
                campo.widget.attrs["class"] = "form-control"
