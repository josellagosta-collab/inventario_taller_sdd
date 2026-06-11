from django.urls import path
from . import views

app_name = "prestamos"

urlpatterns = [
    path("prestamos/nuevo/", views.crear_prestamo, name="crear_prestamo"),
]