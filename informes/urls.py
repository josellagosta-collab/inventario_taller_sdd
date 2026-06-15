from django.urls import path
from . import views

app_name = "informes"

urlpatterns = [
    path("informes/", views.panel_informes, name="panel_informes"),
    path(
        "informes/inventario/",
        views.informe_inventario,
        name="informe_inventario",
    ),
]
