from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class RolesViewsTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin", password="testpass123")

    def test_lista_roles_muestra_roles(self):
        Group.objects.create(name="Profesores")

        response = self.client.get(reverse("usuarios:lista_roles"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Administradores")
        self.assertContains(response, "Profesores")

    def test_crear_rol(self):
        response = self.client.post(
            reverse("usuarios:crear_rol"),
            {
                "name": "Técnicos",
                "permissions": [],
            },
        )

        self.assertRedirects(response, reverse("usuarios:lista_roles"))
        self.assertTrue(Group.objects.filter(name="Técnicos").exists())

    def test_no_elimina_rol_administradores(self):
        response = self.client.post(
            reverse("usuarios:eliminar_rol", args=[self.grupo_admin.id])
        )

        self.assertRedirects(response, reverse("usuarios:lista_roles"))
        self.assertTrue(Group.objects.filter(name="Administradores").exists())

    def test_no_elimina_rol_con_usuarios_asignados(self):
        rol = Group.objects.create(name="Profesores")
        self.usuario.groups.add(rol)

        response = self.client.post(
            reverse("usuarios:eliminar_rol", args=[rol.id])
        )

        self.assertRedirects(response, reverse("usuarios:lista_roles"))
        self.assertTrue(Group.objects.filter(name="Profesores").exists())
