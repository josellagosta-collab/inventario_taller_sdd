from datetime import datetime, timezone as datetime_timezone

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import RegistroAuditoria


class AuditoriaTimezoneTests(TestCase):
    def setUp(self):
        grupo = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )
        self.usuario.groups.add(grupo)
        self.client.login(username="admin", password="testpass123")

    def test_lista_auditoria_muestra_hora_local_de_madrid_en_verano(self):
        registro = RegistroAuditoria.objects.create(
            usuario=self.usuario,
            accion="editar",
            descripcion="Registro de prueba",
        )
        RegistroAuditoria.objects.filter(pk=registro.pk).update(
            fecha=datetime(2026, 6, 15, 10, 0, tzinfo=datetime_timezone.utc)
        )

        response = self.client.get(reverse("auditoria:lista_auditoria"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "15/06/2026 12:00")
