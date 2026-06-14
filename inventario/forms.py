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
            "ubicacion",
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

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get("categoria")
        subcategoria = cleaned_data.get("subcategoria")
        fecha_compra = cleaned_data.get("fecha_compra")
        garantia_hasta = cleaned_data.get("garantia_hasta")
        cantidad = cleaned_data.get("cantidad")
        stock_minimo = cleaned_data.get("stock_minimo")

        if cantidad is not None and cantidad < 0:
            self.add_error("cantidad", "La cantidad no puede ser negativa.")

        if stock_minimo is not None and stock_minimo < 0:
            self.add_error("stock_minimo", "El stock mínimo no puede ser negativo.")

        if subcategoria and categoria and subcategoria.categoria_id != categoria.id:
            self.add_error(
                "subcategoria",
                "La subcategoría seleccionada no pertenece a la categoría indicada."
            )

        if fecha_compra and garantia_hasta and garantia_hasta < fecha_compra:
            self.add_error(
                "garantia_hasta",
                "La fecha de garantía no puede ser anterior a la fecha de compra."
            )

        return cleaned_data
