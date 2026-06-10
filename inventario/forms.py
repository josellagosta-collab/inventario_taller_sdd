from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):

    class Meta:
        model = Material

        fields = [
            "codigo_inventario",
            "nombre",
            "descripcion",
            "categoria",
            "subcategoria",
            "proveedor",
            "marca",
            "modelo",
            "numero_serie",
            "cantidad",
            "stock_minimo",
            "precio_compra",
            "fecha_compra",
            "garantia_hasta",
            "estado",
            "observaciones",
        ]

        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
            "fecha_compra": forms.DateInput(attrs={"type": "date"}),
            "garantia_hasta": forms.DateInput(attrs={"type": "date"}),
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