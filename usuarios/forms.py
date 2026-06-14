from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group, User


class UsuarioCrearForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
    )
    es_administrador = forms.BooleanField(
        label="Pertenece al grupo Administradores",
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_clases_bootstrap(self.fields)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])

        if commit:
            usuario.save()
            actualizar_grupo_administradores(
                usuario,
                self.cleaned_data.get("es_administrador")
            )

        return usuario


class UsuarioEditarForm(forms.ModelForm):
    es_administrador = forms.BooleanField(
        label="Pertenece al grupo Administradores",
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["es_administrador"].initial = self.instance.groups.filter(
                name="Administradores"
            ).exists()

        aplicar_clases_bootstrap(self.fields)

    def save(self, commit=True):
        usuario = super().save(commit=commit)

        if commit:
            actualizar_grupo_administradores(
                usuario,
                self.cleaned_data.get("es_administrador")
            )

        return usuario


class UsuarioPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aplicar_clases_bootstrap(self.fields)


def actualizar_grupo_administradores(usuario, es_administrador):
    grupo, _ = Group.objects.get_or_create(name="Administradores")

    if es_administrador:
        usuario.groups.add(grupo)
    else:
        usuario.groups.remove(grupo)


def aplicar_clases_bootstrap(fields):
    for campo in fields.values():
        campo.widget.attrs["class"] = "form-control"

    for campo in fields.values():
        if isinstance(campo.widget, forms.CheckboxInput):
            campo.widget.attrs["class"] = "form-check-input"
