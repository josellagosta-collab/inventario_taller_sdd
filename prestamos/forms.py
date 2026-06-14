from django import forms
from django.utils import timezone

from inventario.models import Material

from .models import LineaPrestamo, Prestamo, Reserva


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
            "fecha_prevista_devolucion": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_clases_bootstrap(self.fields)

    def clean_fecha_prevista_devolucion(self):
        fecha = self.cleaned_data["fecha_prevista_devolucion"]

        if fecha < timezone.now().date():
            raise forms.ValidationError(
                "La fecha prevista de devolución no puede ser anterior a hoy."
            )

        return fecha


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
        aplicar_clases_bootstrap(self.fields)

    def clean_material(self):
        material = self.cleaned_data["material"]

        if material.estado != "disponible":
            raise forms.ValidationError(
                "Este material no está disponible para préstamo."
            )

        return material

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get("material")
        cantidad = cleaned_data.get("cantidad")

        if cantidad is not None and cantidad <= 0:
            self.add_error("cantidad", "La cantidad debe ser mayor que cero.")

        if material and cantidad and cantidad > material.cantidad:
            self.add_error(
                "cantidad",
                "No puedes prestar una cantidad superior a la disponible."
            )

        return cleaned_data


class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = [
            "usuario_reserva",
            "profesor_responsable",
            "material",
            "cantidad",
            "fecha_prevista_recogida",
            "observaciones",
        ]
        widgets = {
            "fecha_prevista_recogida": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["material"].queryset = Material.objects.filter(
            estado="disponible"
        )
        aplicar_clases_bootstrap(self.fields)

    def clean_fecha_prevista_recogida(self):
        fecha = self.cleaned_data["fecha_prevista_recogida"]

        if fecha < timezone.now().date():
            raise forms.ValidationError(
                "La fecha prevista de recogida no puede ser anterior a hoy."
            )

        return fecha

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get("material")
        cantidad = cleaned_data.get("cantidad")

        if cantidad is not None and cantidad <= 0:
            self.add_error("cantidad", "La cantidad debe ser mayor que cero.")

        if material and material.estado != "disponible":
            self.add_error(
                "material",
                "Este material no está disponible para reserva."
            )

        if material and cantidad and cantidad > material.cantidad:
            self.add_error(
                "cantidad",
                "No puedes reservar una cantidad superior a la disponible."
            )

        return cleaned_data


class ReservaMaterialForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = [
            "usuario_reserva",
            "profesor_responsable",
            "cantidad",
            "fecha_prevista_recogida",
            "observaciones",
        ]
        widgets = {
            "fecha_prevista_recogida": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_clases_bootstrap(self.fields)

    def clean_fecha_prevista_recogida(self):
        fecha = self.cleaned_data["fecha_prevista_recogida"]

        if fecha < timezone.now().date():
            raise forms.ValidationError(
                "La fecha prevista de recogida no puede ser anterior a hoy."
            )

        return fecha

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get("cantidad")

        if cantidad is not None and cantidad <= 0:
            self.add_error("cantidad", "La cantidad debe ser mayor que cero.")

        return cleaned_data


def aplicar_clases_bootstrap(fields):
    for campo in fields.values():
        campo.widget.attrs["class"] = "form-control"

    for campo in fields.values():
        if isinstance(campo.widget, (forms.Select, forms.SelectMultiple)):
            campo.widget.attrs["class"] = "form-select"
