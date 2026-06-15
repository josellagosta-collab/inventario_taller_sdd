from datetime import timedelta

from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from inventario.models import Categoria, Material

from .forms import LineaPrestamoForm, PrestamoForm, ReservaForm, ReservaMaterialForm
from .models import LineaPrestamo, Prestamo, Reserva


class PrestamosModelTests(TestCase):
    def setUp(self):
        self.profesor = User.objects.create_user(username="profesor")
        self.alumno = User.objects.create_user(username="alumno")
        self.categoria = Categoria.objects.create(nombre="Redes")
        self.material = Material.objects.create(
            codigo_inventario="PRE-001",
            nombre="Router de préstamo",
            categoria=self.categoria,
            cantidad=1,
        )

    def test_prestamo_activo_detecta_retraso(self):
        prestamo = Prestamo.objects.create(
            usuario_receptor=self.alumno,
            profesor_responsable=self.profesor,
            fecha_prevista_devolucion=timezone.now().date() - timedelta(days=1),
            estado="activo",
        )

        self.assertTrue(prestamo.esta_retrasado())

    def test_prestamo_devuelto_no_se_considera_retrasado(self):
        prestamo = Prestamo.objects.create(
            usuario_receptor=self.alumno,
            profesor_responsable=self.profesor,
            fecha_prevista_devolucion=timezone.now().date() - timedelta(days=1),
            estado="devuelto",
        )

        self.assertFalse(prestamo.esta_retrasado())

    def test_linea_prestamo_y_reserva_devuelven_texto_legible(self):
        prestamo = Prestamo.objects.create(
            usuario_receptor=self.alumno,
            profesor_responsable=self.profesor,
            fecha_prevista_devolucion=timezone.now().date() + timedelta(days=7),
        )
        linea = LineaPrestamo.objects.create(
            prestamo=prestamo,
            material=self.material,
            cantidad=2,
        )
        reserva = Reserva.objects.create(
            usuario_reserva=self.alumno,
            profesor_responsable=self.profesor,
            material=self.material,
            fecha_prevista_recogida=timezone.now().date() + timedelta(days=1),
        )

        self.assertEqual(str(linea), "Router de préstamo x 2")
        self.assertEqual(str(reserva), f"Reserva {reserva.id} - Router de préstamo")

    def test_reserva_activa_detecta_caducidad(self):
        reserva = Reserva.objects.create(
            usuario_reserva=self.alumno,
            profesor_responsable=self.profesor,
            material=self.material,
            fecha_prevista_recogida=timezone.now().date() - timedelta(days=1),
            estado="activa",
        )

        self.assertTrue(reserva.esta_caducada())


class PrestamosFormTests(TestCase):
    def setUp(self):
        self.profesor = User.objects.create_user(username="profesor_form")
        self.alumno = User.objects.create_user(username="alumno_form")
        self.categoria = Categoria.objects.create(nombre="Componentes")
        self.material_disponible = Material.objects.create(
            codigo_inventario="FORM-PRE-001",
            nombre="Material disponible",
            categoria=self.categoria,
            cantidad=2,
            estado="disponible",
        )
        self.material_prestado = Material.objects.create(
            codigo_inventario="FORM-PRE-002",
            nombre="Material prestado",
            categoria=self.categoria,
            cantidad=1,
            estado="prestado",
        )

    def test_prestamo_rechaza_fecha_prevista_pasada(self):
        form = PrestamoForm(data={
            "usuario_receptor": self.alumno.id,
            "profesor_responsable": self.profesor.id,
            "fecha_prevista_devolucion": (
                timezone.now().date() - timedelta(days=1)
            ).isoformat(),
            "observaciones": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("fecha_prevista_devolucion", form.errors)

    def test_linea_prestamo_rechaza_cantidad_superior_a_disponible(self):
        form = LineaPrestamoForm(data={
            "material": self.material_disponible.id,
            "cantidad": 3,
        })

        self.assertFalse(form.is_valid())
        self.assertIn("cantidad", form.errors)

    def test_linea_prestamo_solo_lista_material_disponible(self):
        form = LineaPrestamoForm()

        self.assertIn(self.material_disponible, form.fields["material"].queryset)
        self.assertNotIn(self.material_prestado, form.fields["material"].queryset)

    def test_reserva_rechaza_fecha_recogida_pasada(self):
        form = ReservaForm(data={
            "usuario_reserva": self.alumno.id,
            "profesor_responsable": self.profesor.id,
            "material": self.material_disponible.id,
            "cantidad": 1,
            "fecha_prevista_recogida": (
                timezone.now().date() - timedelta(days=1)
            ).isoformat(),
            "observaciones": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("fecha_prevista_recogida", form.errors)

    def test_reserva_material_rechaza_cantidad_cero(self):
        form = ReservaMaterialForm(data={
            "usuario_reserva": self.alumno.id,
            "profesor_responsable": self.profesor.id,
            "cantidad": 0,
            "fecha_prevista_recogida": (
                timezone.now().date() + timedelta(days=1)
            ).isoformat(),
            "observaciones": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("cantidad", form.errors)


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


class RendimientoPrestamosTests(TestCase):
    def setUp(self):
        self.profesor = User.objects.create_user(
            username="profesor_perf",
            password="testpass123",
        )
        self.alumno = User.objects.create_user(username="alumno_perf")
        self.client.force_login(self.profesor)
        self.categoria = Categoria.objects.create(nombre="Préstamos rendimiento")
        self.materiales = [
            Material.objects.create(
                codigo_inventario=f"PRE-PERF-{indice:03d}",
                nombre=f"Material préstamo rendimiento {indice}",
                categoria=self.categoria,
                cantidad=1,
            )
            for indice in range(25)
        ]

        for material in self.materiales:
            prestamo = Prestamo.objects.create(
                usuario_receptor=self.alumno,
                profesor_responsable=self.profesor,
                fecha_prevista_devolucion=timezone.now().date() + timedelta(days=7),
                estado="activo",
            )
            LineaPrestamo.objects.create(
                prestamo=prestamo,
                material=material,
                cantidad=1,
            )

    def test_lista_prestamos_mantiene_consultas_acotadas_con_lineas(self):
        with CaptureQueriesContext(connection) as contexto:
            response = self.client.get(reverse("prestamos:lista_prestamos"))

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(
            len(contexto),
            16,
            f"Se ejecutaron {len(contexto)} consultas, máximo esperado 16.",
        )
