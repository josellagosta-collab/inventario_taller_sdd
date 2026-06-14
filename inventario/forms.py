from django import forms
from django.utils import timezone

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

        self.fields["cantidad"].widget.attrs["min"] = "0"
        self.fields["stock_minimo"].widget.attrs["min"] = "0"
        self.fields["precio_compra"].widget.attrs["min"] = "0"
        self.fields["precio_compra"].widget.attrs["step"] = "0.01"

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

    def clean_codigo_inventario(self):
        codigo = self.cleaned_data.get("codigo_inventario", "").strip()

        if not codigo:
            return codigo

        materiales = Material.objects.filter(codigo_inventario__iexact=codigo)

        if self.instance.pk:
            materiales = materiales.exclude(pk=self.instance.pk)

        if materiales.exists():
            raise forms.ValidationError(
                "Ya existe un material con este código de inventario."
            )

        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "").strip()

        if not nombre:
            raise forms.ValidationError("El nombre del material es obligatorio.")

        return nombre

    def clean_numero_serie(self):
        numero_serie = self.cleaned_data.get("numero_serie")

        if not numero_serie:
            return numero_serie

        numero_serie = numero_serie.strip()

        if not numero_serie:
            return ""

        materiales = Material.objects.filter(numero_serie__iexact=numero_serie)

        if self.instance.pk:
            materiales = materiales.exclude(pk=self.instance.pk)

        if materiales.exists():
            raise forms.ValidationError(
                "Ya existe un material con este número de serie."
            )

        return numero_serie

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get("categoria")
        subcategoria = cleaned_data.get("subcategoria")
        fecha_compra = cleaned_data.get("fecha_compra")
        garantia_hasta = cleaned_data.get("garantia_hasta")
        cantidad = cleaned_data.get("cantidad")
        stock_minimo = cleaned_data.get("stock_minimo")
        precio_compra = cleaned_data.get("precio_compra")
        estado = cleaned_data.get("estado")
        hoy = timezone.now().date()

        if cantidad is not None and cantidad < 0:
            self.add_error("cantidad", "La cantidad no puede ser negativa.")

        if stock_minimo is not None and stock_minimo < 0:
            self.add_error("stock_minimo", "El stock mínimo no puede ser negativo.")

        if precio_compra is not None and precio_compra < 0:
            self.add_error("precio_compra", "El precio de compra no puede ser negativo.")

        if subcategoria and categoria and subcategoria.categoria_id != categoria.id:
            self.add_error(
                "subcategoria",
                "La subcategoría seleccionada no pertenece a la categoría indicada."
            )

        if fecha_compra and fecha_compra > hoy:
            self.add_error(
                "fecha_compra",
                "La fecha de compra no puede ser futura."
            )

        if fecha_compra and garantia_hasta and garantia_hasta < fecha_compra:
            self.add_error(
                "garantia_hasta",
                "La fecha de garantía no puede ser anterior a la fecha de compra."
            )

        if cantidad == 0 and estado in ["disponible", "reservado", "prestado"]:
            self.add_error(
                "cantidad",
                "La cantidad debe ser mayor que cero para materiales disponibles, reservados o prestados."
            )

        if self.instance.pk:
            tiene_prestamo_activo = self.instance.lineas_prestamo.filter(
                prestamo__estado="activo"
            ).exists()

            if tiene_prestamo_activo and estado not in ["prestado", "perdido"]:
                self.add_error(
                    "estado",
                    "Un material con préstamo activo debe mantenerse como prestado o perdido."
                )

        return cleaned_data
