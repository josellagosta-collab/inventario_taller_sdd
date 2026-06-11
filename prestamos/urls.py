from django.urls import path
from . import views

app_name = "prestamos"

urlpatterns = [
    path("prestamos/", views.lista_prestamos, name="lista_prestamos"),
    path("prestamos/nuevo/", views.crear_prestamo, name="crear_prestamo"),
]