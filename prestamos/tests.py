from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from inventario.models import Categoria, Material

from .models import LineaPrestamo, Prestamo


class HistoricoPrestamosTests(TestCase):
    def setUp(self):
        self.profesor = User.objects.create_user(
            username="profesor",
            password="testpass123",
        )
        self.alumno = User.objects.create_user(
            username="alumno",
            password="testpass123",
        )
        self.client.login(username="profesor", password="testpass123")
        self.categoria = Categoria.objects.create(nombre="Redes")
        self.material_devuelto = Material.objects.create(
            codigo_inventario="SW-001",
            nombre="Switch Cisco",
            categoria=self.categoria,
            cantidad=1,
        )
        self.material_activo = Material.objects.create(
            codigo_inventario="RT-001",
            nombre="Router activo",
            categoria=self.categoria,
            cantidad=1,
        )
        self.material_retrasado = Material.objects.create(
            codigo_inventario="FW-001",
            nombre="Firewall retrasado",
            categoria=self.categoria,
            cantidad=1,
        )

    def crear_prestamo(self, material, estado, fecha_prevista, fecha_devolucion=None):
        prestamo = Prestamo.objects.create(
            usuario_receptor=self.alumno,
            profesor_responsable=self.profesor,
            fecha_prevista_devolucion=fecha_prevista,
            fecha_devolucion_real=fecha_devolucion,
            estado=estado,
        )
        LineaPrestamo.objects.create(
            prestamo=prestamo,
            material=material,
            cantidad=1,
        )
        return prestamo

    def test_historico_muestra_devueltos_y_activos_retrasados(self):
        hoy = timezone.now().date()
        self.crear_prestamo(
            self.material_devuelto,
            "devuelto",
            hoy - timedelta(days=3),
            fecha_devolucion=hoy - timedelta(days=1),
        )
        self.crear_prestamo(
            self.material_activo,
            "activo",
            hoy + timedelta(days=5),
        )
        self.crear_prestamo(
            self.material_retrasado,
            "activo",
            hoy - timedelta(days=2),
        )

        response = self.client.get(reverse("prestamos:historico_prestamos"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Switch Cisco")
        self.assertContains(response, "Firewall retrasado")
        self.assertNotContains(response, "Router activo")

    def test_historico_filtra_por_busqueda_de_material(self):
        hoy = timezone.now().date()
        self.crear_prestamo(
            self.material_devuelto,
            "devuelto",
            hoy - timedelta(days=3),
            fecha_devolucion=hoy - timedelta(days=1),
        )
        self.crear_prestamo(
            self.material_retrasado,
            "activo",
            hoy - timedelta(days=2),
        )

        response = self.client.get(
            reverse("prestamos:historico_prestamos"),
            {"busqueda": "Cisco"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Switch Cisco")
        self.assertNotContains(response, "Firewall retrasado")
