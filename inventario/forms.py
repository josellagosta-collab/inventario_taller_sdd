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