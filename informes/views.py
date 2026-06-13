from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def panel_informes(request):
    return render(request, "informes/panel_informes.html")