from django.urls import path

from . import views

app_name = "auditoria"

urlpatterns = [
    path("auditoria/", views.lista_auditoria, name="lista_auditoria"),
]
