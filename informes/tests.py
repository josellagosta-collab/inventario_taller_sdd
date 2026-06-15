from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from incidencias.models import Incidencia
from inventario.models import Categoria, Material, MovimientoInventario
from prestamos.models import LineaPrestamo, Prestamo, Reserva
from usuarios.models import PerfilUsuario


class ExportarCsvTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin_csv",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.usuario)
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin_csv", password="testpass123")

        self.categoria = Categoria.objects.create(nombre="Redes")
        self.material = Material.objects.create(
            codigo_inventario="CSV-001",
            nombre="Router CSV",
            categoria=self.categoria,
            cantidad=1,
        )
        self.otro_material = Material.objects.create(
            codigo_inventario="CSV-002",
            nombre="Switch oculto",
            categoria=self.categoria,
            cantidad=1,
        )
        MovimientoInventario.objects.create(
            material=self.material,
            tipo="alta",
            usuario=self.usuario,
            descripcion="Alta CSV",
        )
        Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="Incidencia CSV",
            descripcion="Prueba de exportación",
            prioridad="alta",
        )
        self.prestamo = Prestamo.objects.create(
            usuario_receptor=self.usuario,
            profesor_responsable=self.usuario,
            fecha_prevista_devolucion=timezone.now().date() + timedelta(days=7),
            estado="activo",
        )
        LineaPrestamo.objects.create(
            prestamo=self.prestamo,
            material=self.material,
            cantidad=1,
        )
        Reserva.objects.create(
            usuario_reserva=self.usuario,
            profesor_responsable=self.usuario,
            material=self.material,
            cantidad=1,
            fecha_prevista_recogida=timezone.now().date() + timedelta(days=1),
            estado="activa",
        )

    def assert_csv_response(self, response, filename, contenido):
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn(filename, response["Content-Disposition"])
        texto = response.content.decode("utf-8-sig")
        self.assertIn(contenido, texto)

    def test_exportar_materiales_csv_respeta_filtro_busqueda(self):
        response = self.client.get(
            reverse("inventario:exportar_materiales_csv"),
            {"busqueda": "Router"},
        )

        self.assert_csv_response(response, "inventario.csv", "Router CSV")
        self.assertNotIn("Switch oculto", response.content.decode("utf-8-sig"))

    def test_exportar_movimientos_csv(self):
        response = self.client.get(reverse("inventario:exportar_movimientos_csv"))

        self.assert_csv_response(response, "movimientos.csv", "Alta CSV")

    def test_exportar_incidencias_csv(self):
        response = self.client.get(reverse("incidencias:exportar_incidencias_csv"))

        self.assert_csv_response(response, "incidencias.csv", "Incidencia CSV")

    def test_exportar_prestamos_csv(self):
        response = self.client.get(reverse("prestamos:exportar_prestamos_csv"))

        self.assert_csv_response(response, "prestamos.csv", "Router CSV x 1")

    def test_exportar_reservas_csv(self):
        response = self.client.get(reverse("prestamos:exportar_reservas_csv"))

        self.assert_csv_response(response, "reservas.csv", "Router CSV")
