from django import forms

from .models import Ubicacion


class UbicacionForm(forms.ModelForm):

    class Meta:
        model = Ubicacion
        fields = [
            "edificio",
            "aula",
            "armario",
            "estanteria",
            "caja",
            "posicion",
            "descripcion",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

        for campo in self.fields.values():
            if isinstance(campo.widget, forms.Select):
                campo.widget.attrs["class"] = "form-select"

    def clean(self):
        cleaned_data = super().clean()
        edificio = cleaned_data.get("edificio")
        aula = cleaned_data.get("aula")
        armario = cleaned_data.get("armario")
        estanteria = cleaned_data.get("estanteria")
        caja = cleaned_data.get("caja")

        if aula and edificio and aula.edificio_id != edificio.id:
            self.add_error(
                "aula",
                "El aula seleccionada no pertenece al edificio indicado."
            )

        if armario and not aula:
            self.add_error(
                "armario",
                "Para seleccionar un armario también debes seleccionar un aula."
            )

        if armario and aula and armario.aula_id != aula.id:
            self.add_error(
                "armario",
                "El armario seleccionado no pertenece al aula indicada."
            )

        if estanteria and not armario:
            self.add_error(
                "estanteria",
                "Para seleccionar una estantería también debes seleccionar un armario."
            )

        if estanteria and armario and estanteria.armario_id != armario.id:
            self.add_error(
                "estanteria",
                "La estantería seleccionada no pertenece al armario indicado."
            )

        if caja and not estanteria:
            self.add_error(
                "caja",
                "Para seleccionar una caja también debes seleccionar una estantería."
            )

        if caja and estanteria and caja.estanteria_id != estanteria.id:
            self.add_error(
                "caja",
                "La caja seleccionada no pertenece a la estantería indicada."
            )

        return cleaned_data
