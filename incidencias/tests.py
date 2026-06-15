from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from inventario.models import Categoria, Material

from .forms import IncidenciaForm, ResolverIncidenciaForm
from .models import ComentarioIncidencia, Incidencia


class IncidenciasModelTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="tecnico")
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="INC-001",
            nombre="Equipo averiado",
            categoria=self.categoria,
            cantidad=1,
        )

    def test_incidencia_tiene_estado_y_prioridad_por_defecto(self):
        incidencia = Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="No arranca",
            descripcion="El equipo no enciende",
        )

        self.assertEqual(incidencia.estado, "abierta")
        self.assertEqual(incidencia.prioridad, "media")
        self.assertEqual(str(incidencia), "No arranca - Equipo averiado")

    def test_comentario_incidencia_devuelve_titulo_de_incidencia(self):
        incidencia = Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="Pantalla rota",
            descripcion="Cristal dañado",
        )
        comentario = ComentarioIncidencia.objects.create(
            incidencia=incidencia,
            usuario=self.usuario,
            comentario="Pendiente de repuesto",
        )

        self.assertEqual(str(comentario), "Comentario en Pantalla rota")
        self.assertEqual(incidencia.comentarios.count(), 1)


class IncidenciasFormTests(TestCase):
    def test_incidencia_form_valido(self):
        form = IncidenciaForm(data={
            "titulo": "No enciende",
            "descripcion": "El equipo no arranca al pulsar el botón.",
            "prioridad": "alta",
        })

        self.assertTrue(form.is_valid())

    def test_incidencia_form_requiere_titulo(self):
        form = IncidenciaForm(data={
            "titulo": "",
            "descripcion": "Descripción de la incidencia",
            "prioridad": "media",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("titulo", form.errors)

    def test_resolver_incidencia_requiere_solucion(self):
        form = ResolverIncidenciaForm(data={
            "solucion": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("solucion", form.errors)


class IncidenciasViewTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin_incidencias_view",
            password="testpass123",
        )
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin_incidencias_view", password="testpass123")
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="INC-VIEW-001",
            nombre="Equipo incidencias",
            categoria=self.categoria,
            cantidad=1,
        )
        self.incidencia_visible = Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="Fallo visible",
            descripcion="No enciende",
            prioridad="alta",
            estado="abierta",
        )
        self.incidencia_oculta = Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="Fallo oculto",
            descripcion="Ya resuelto",
            prioridad="baja",
            estado="cerrada",
        )

    def test_lista_incidencias_filtra_por_estado(self):
        response = self.client.get(
            reverse("incidencias:lista_incidencias"),
            {"estado": "abierta"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fallo visible")
        self.assertNotContains(response, "Fallo oculto")

    def test_detalle_incidencia_muestra_datos(self):
        ComentarioIncidencia.objects.create(
            incidencia=self.incidencia_visible,
            usuario=self.usuario,
            comentario="Comentario visible",
        )

        response = self.client.get(
            reverse(
                "incidencias:detalle_incidencia",
                args=[self.incidencia_visible.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fallo visible")
        self.assertContains(response, "Comentario visible")

    def test_resolver_incidencia_get_muestra_formulario(self):
        response = self.client.get(
            reverse(
                "incidencias:resolver_incidencia",
                args=[self.incidencia_visible.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fallo visible")
