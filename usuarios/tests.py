from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import PerfilUsuario


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


class PerfilUsuarioTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin", password="testpass123")

    def test_crea_perfil_automaticamente_al_crear_usuario(self):
        usuario = User.objects.create_user(
            username="profesor",
            password="testpass123",
        )

        self.assertTrue(PerfilUsuario.objects.filter(user=usuario).exists())

    def test_crear_usuario_guarda_datos_de_perfil(self):
        response = self.client.post(
            reverse("usuarios:crear_usuario"),
            {
                "username": "tecnico",
                "first_name": "Ana",
                "last_name": "Lopez",
                "email": "ana@example.com",
                "is_active": "on",
                "password1": "testpass123",
                "password2": "testpass123",
                "tipo_usuario": PerfilUsuario.TIPO_TECNICO,
                "departamento": "Hardware",
                "telefono": "600123123",
                "puede_recibir_prestamos": "on",
                "observaciones": "Responsable de reparaciones",
            },
        )

        self.assertRedirects(response, reverse("usuarios:lista_usuarios"))
        perfil = User.objects.get(username="tecnico").perfil
        self.assertEqual(perfil.tipo_usuario, PerfilUsuario.TIPO_TECNICO)
        self.assertEqual(perfil.departamento, "Hardware")
        self.assertEqual(perfil.telefono, "600123123")
        self.assertTrue(perfil.puede_recibir_prestamos)
