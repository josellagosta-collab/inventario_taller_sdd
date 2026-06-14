from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/nuevo/", views.crear_usuario, name="crear_usuario"),
    path("usuarios/<int:usuario_id>/editar/", views.editar_usuario, name="editar_usuario"),
    path("usuarios/<int:usuario_id>/password/", views.cambiar_password_usuario, name="cambiar_password_usuario"),
    path("usuarios/<int:usuario_id>/desactivar/", views.desactivar_usuario, name="desactivar_usuario"),
]
