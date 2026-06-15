from io import StringIO

from django.contrib.auth.models import Group, Permission, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from inventario.models import Categoria, Material

from .forms import RolForm, UsuarioCrearForm, UsuarioEditarForm
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


class UsuariosFormTests(TestCase):
    def test_usuario_crear_form_rechaza_passwords_distintas(self):
        form = UsuarioCrearForm(data={
            "username": "usuario_form",
            "first_name": "",
            "last_name": "",
            "email": "usuario@example.com",
            "is_active": "on",
            "password1": "testpass123",
            "password2": "otra-pass",
            "tipo_usuario": PerfilUsuario.TIPO_PROFESOR,
            "departamento": "",
            "telefono": "",
            "puede_recibir_prestamos": "on",
            "observaciones": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_usuario_crear_form_guarda_perfil_y_grupo_admin(self):
        form = UsuarioCrearForm(data={
            "username": "admin_form",
            "first_name": "Admin",
            "last_name": "Form",
            "email": "admin@example.com",
            "is_active": "on",
            "password1": "testpass123",
            "password2": "testpass123",
            "es_administrador": "on",
            "tipo_usuario": PerfilUsuario.TIPO_ADMINISTRADOR,
            "departamento": "Sistemas",
            "telefono": "600000000",
            "puede_recibir_prestamos": "on",
            "observaciones": "Usuario creado desde test",
        })

        self.assertTrue(form.is_valid())
        usuario = form.save()
        perfil = PerfilUsuario.objects.get(user=usuario)

        self.assertTrue(usuario.check_password("testpass123"))
        self.assertTrue(usuario.groups.filter(name="Administradores").exists())
        self.assertEqual(perfil.tipo_usuario, PerfilUsuario.TIPO_ADMINISTRADOR)
        self.assertEqual(perfil.departamento, "Sistemas")

    def test_usuario_editar_form_actualiza_perfil_y_quita_admin(self):
        grupo = Group.objects.create(name="Administradores")
        usuario = User.objects.create_user(username="usuario_editar")
        usuario.groups.add(grupo)
        perfil, _ = PerfilUsuario.objects.get_or_create(user=usuario)
        perfil.tipo_usuario = PerfilUsuario.TIPO_PROFESOR
        perfil.departamento = "Inicial"
        perfil.save()

        form = UsuarioEditarForm(
            data={
                "first_name": "Nombre",
                "last_name": "Apellido",
                "email": "editado@example.com",
                "is_active": "on",
                "tipo_usuario": PerfilUsuario.TIPO_TECNICO,
                "departamento": "Hardware",
                "telefono": "611111111",
                "puede_recibir_prestamos": "",
                "observaciones": "Actualizado",
            },
            instance=usuario,
        )

        self.assertTrue(form.is_valid())
        usuario = form.save()
        usuario.refresh_from_db()
        perfil.refresh_from_db()

        self.assertFalse(usuario.groups.filter(name="Administradores").exists())
        self.assertEqual(perfil.tipo_usuario, PerfilUsuario.TIPO_TECNICO)
        self.assertEqual(perfil.departamento, "Hardware")

    def test_rol_form_permite_crear_rol_sin_permisos(self):
        form = RolForm(data={
            "name": "Inventario lectura",
            "permissions": [],
        })

        self.assertTrue(form.is_valid())


class LogoutTests(TestCase):
    def test_logout_redirige_a_pagina_de_sesion_cerrada(self):
        User.objects.create_user(
            username="usuario",
            password="testpass123",
        )
        self.client.login(username="usuario", password="testpass123")

        response = self.client.post(reverse("logout"))

        self.assertRedirects(
            response,
            reverse("usuarios:logout_done"),
            fetch_redirect_response=False,
        )

    def test_pagina_logout_done_muestra_confirmacion(self):
        response = self.client.get(reverse("usuarios:logout_done"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has cerrado sesión correctamente.")


class InicializarGruposCommandTests(TestCase):
    def test_crea_grupos_base_con_permisos(self):
        salida = StringIO()

        call_command("inicializar_grupos", stdout=salida)

        for nombre_grupo in ["Administradores", "Profesores", "Técnicos", "Alumnos"]:
            self.assertTrue(Group.objects.filter(name=nombre_grupo).exists())

        total_permisos = Permission.objects.count()
        administradores = Group.objects.get(name="Administradores")
        profesores = Group.objects.get(name="Profesores")
        tecnicos = Group.objects.get(name="Técnicos")
        alumnos = Group.objects.get(name="Alumnos")

        self.assertEqual(administradores.permissions.count(), total_permisos)
        self.assertGreater(profesores.permissions.count(), 0)
        self.assertGreater(tecnicos.permissions.count(), 0)
        self.assertGreater(alumnos.permissions.count(), 0)
        self.assertIn("Inicialización de grupos completada", salida.getvalue())

    def test_asigna_usuario_al_grupo_administradores(self):
        usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )

        call_command("inicializar_grupos", admin_user=["admin"], stdout=StringIO())

        self.assertTrue(
            usuario.groups.filter(name="Administradores").exists()
        )


class PermisosViewsTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username="usuario_normal",
            password="testpass123",
        )
        self.superusuario = User.objects.create_superuser(
            username="superadmin",
            password="testpass123",
            email="superadmin@example.com",
        )
        self.categoria = Categoria.objects.create(nombre="Permisos")
        self.material = Material.objects.create(
            codigo_inventario="PERM-001",
            nombre="Material permisos",
            categoria=self.categoria,
            cantidad=1,
        )

    def urls_admin(self):
        return [
            reverse("usuarios:lista_usuarios"),
            reverse("usuarios:lista_roles"),
            reverse("inventario:crear_material"),
            reverse("inventario:editar_material", args=[self.material.id]),
            reverse("inventario:trasladar_material", args=[self.material.id]),
            reverse("inventario:retirar_material", args=[self.material.id]),
            reverse("ubicaciones:crear_ubicacion"),
            reverse("documentos:subir_documento", args=[self.material.id]),
            reverse("prestamos:crear_prestamo"),
            reverse("incidencias:crear_incidencia", args=[self.material.id]),
            reverse("mantenimiento:crear_mantenimiento_material", args=[self.material.id]),
            reverse("auditoria:lista_auditoria"),
            reverse("informes:panel_informes"),
        ]

    def test_usuario_autenticado_sin_grupo_admin_recibe_403_en_vistas_admin(self):
        self.client.login(username="usuario_normal", password="testpass123")

        for url in self.urls_admin():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_usuario_anonimo_redirige_a_login_en_vistas_admin(self):
        for url in self.urls_admin():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn("/login/", response["Location"])

    def test_superusuario_accede_a_vistas_admin_sin_grupo(self):
        self.client.login(username="superadmin", password="testpass123")

        for url in self.urls_admin():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_usuario_autenticado_accede_a_vistas_de_consulta(self):
        self.client.login(username="usuario_normal", password="testpass123")

        urls_consulta = [
            reverse("inventario:lista_materiales"),
            reverse("inventario:detalle_material", args=[self.material.id]),
            reverse("prestamos:lista_prestamos"),
            reverse("incidencias:lista_incidencias"),
            reverse("documentos:lista_documentos"),
        ]

        for url in urls_consulta:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
