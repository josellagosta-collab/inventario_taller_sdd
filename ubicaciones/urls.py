from django.urls import path

from . import views

app_name = "ubicaciones"

urlpatterns = [
    path("ubicaciones/", views.lista_ubicaciones, name="lista_ubicaciones"),
    path("ubicaciones/nueva/", views.crear_ubicacion, name="crear_ubicacion"),
    path("ubicaciones/<int:ubicacion_id>/editar/", views.editar_ubicacion, name="editar_ubicacion"),
    path("ubicaciones/<int:ubicacion_id>/eliminar/", views.eliminar_ubicacion, name="eliminar_ubicacion"),
]
