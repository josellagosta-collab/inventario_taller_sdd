from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.decorators import pertenece_a_grupo


@login_required
@pertenece_a_grupo("Administradores")
def panel_informes(request):
    return render(request, "informes/panel_informes.html")
