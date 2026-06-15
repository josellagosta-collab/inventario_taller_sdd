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


class InformeInventarioTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin_informe",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.usuario)
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin_informe", password="testpass123")

        self.categoria = Categoria.objects.create(nombre="Herramientas")
        self.material_visible = Material.objects.create(
            codigo_inventario="INF-001",
            nombre="Osciloscopio",
            categoria=self.categoria,
            cantidad=1,
            stock_minimo=2,
            precio_compra="350.00",
        )
        self.material_oculto = Material.objects.create(
            codigo_inventario="INF-002",
            nombre="Multímetro",
            categoria=self.categoria,
            cantidad=4,
            stock_minimo=1,
            precio_compra="25.00",
        )

    def test_panel_informes_enlaza_informe_inventario(self):
        response = self.client.get(reverse("informes:panel_informes"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ver informe de inventario")
        self.assertContains(response, reverse("informes:informe_inventario"))

    def test_informe_inventario_muestra_resumen_y_materiales(self):
        response = self.client.get(reverse("informes:informe_inventario"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Informe de inventario")
        self.assertContains(response, "Osciloscopio")
        self.assertContains(response, "Multímetro")
        self.assertContains(response, "Stock bajo")

    def test_informe_inventario_filtra_por_busqueda(self):
        response = self.client.get(
            reverse("informes:informe_inventario"),
            {"busqueda": "Osciloscopio"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Osciloscopio")
        self.assertNotContains(response, "Multímetro")


class InformePrestamosTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.profesor = User.objects.create_user(
            username="profesor_informe",
            password="testpass123",
        )
        self.alumno = User.objects.create_user(username="alumno_informe")
        PerfilUsuario.objects.get_or_create(user=self.profesor)
        self.profesor.groups.add(self.grupo_admin)
        self.client.login(username="profesor_informe", password="testpass123")

        self.categoria = Categoria.objects.create(nombre="Redes")
        self.material_visible = Material.objects.create(
            codigo_inventario="PRE-INF-001",
            nombre="Router préstamo",
            categoria=self.categoria,
            cantidad=1,
        )
        self.material_oculto = Material.objects.create(
            codigo_inventario="PRE-INF-002",
            nombre="Switch préstamo",
            categoria=self.categoria,
            cantidad=1,
        )
        self.prestamo_retrasado = self.crear_prestamo(
            self.material_visible,
            "activo",
            timezone.now().date() - timedelta(days=2),
        )
        self.prestamo_futuro = self.crear_prestamo(
            self.material_oculto,
            "activo",
            timezone.now().date() + timedelta(days=5),
        )

    def crear_prestamo(self, material, estado, fecha_prevista):
        prestamo = Prestamo.objects.create(
            usuario_receptor=self.alumno,
            profesor_responsable=self.profesor,
            fecha_prevista_devolucion=fecha_prevista,
            estado=estado,
        )
        LineaPrestamo.objects.create(
            prestamo=prestamo,
            material=material,
            cantidad=1,
        )
        return prestamo

    def test_panel_informes_enlaza_informe_prestamos(self):
        response = self.client.get(reverse("informes:panel_informes"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ver informe de préstamos")
        self.assertContains(response, reverse("informes:informe_prestamos"))

    def test_informe_prestamos_muestra_resumen_y_prestamos(self):
        response = self.client.get(reverse("informes:informe_prestamos"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Informe de préstamos")
        self.assertContains(response, "Router préstamo")
        self.assertContains(response, "Switch préstamo")
        self.assertContains(response, "Retrasados")

    def test_informe_prestamos_filtra_por_busqueda(self):
        response = self.client.get(
            reverse("informes:informe_prestamos"),
            {"busqueda": "Router"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Router préstamo")
        self.assertNotContains(response, "Switch préstamo")

    def test_informe_prestamos_filtra_retrasados(self):
        response = self.client.get(
            reverse("informes:informe_prestamos"),
            {"retrasados": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Router préstamo")
        self.assertNotContains(response, "Switch préstamo")


class InformeIncidenciasTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin_incidencias",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.usuario)
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin_incidencias", password="testpass123")

        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material_visible = Material.objects.create(
            codigo_inventario="INC-INF-001",
            nombre="Equipo incidencia",
            categoria=self.categoria,
            cantidad=1,
        )
        self.material_oculto = Material.objects.create(
            codigo_inventario="INC-INF-002",
            nombre="Equipo cerrado",
            categoria=self.categoria,
            cantidad=1,
        )
        Incidencia.objects.create(
            material=self.material_visible,
            usuario=self.usuario,
            titulo="Fallo visible",
            descripcion="No arranca",
            prioridad="critica",
            estado="abierta",
        )
        Incidencia.objects.create(
            material=self.material_oculto,
            usuario=self.usuario,
            titulo="Fallo cerrado",
            descripcion="Resuelto",
            prioridad="baja",
            estado="cerrada",
        )

    def test_panel_informes_enlaza_informe_incidencias(self):
        response = self.client.get(reverse("informes:panel_informes"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ver informe de incidencias")
        self.assertContains(response, reverse("informes:informe_incidencias"))

    def test_informe_incidencias_muestra_resumen_e_incidencias(self):
        response = self.client.get(reverse("informes:informe_incidencias"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Informe de incidencias")
        self.assertContains(response, "Fallo visible")
        self.assertContains(response, "Fallo cerrado")
        self.assertContains(response, "Críticas activas")

    def test_informe_incidencias_filtra_por_busqueda(self):
        response = self.client.get(
            reverse("informes:informe_incidencias"),
            {"busqueda": "visible"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fallo visible")
        self.assertNotContains(response, "Fallo cerrado")

    def test_informe_incidencias_filtra_abiertas(self):
        response = self.client.get(
            reverse("informes:informe_incidencias"),
            {"abiertas": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fallo visible")
        self.assertNotContains(response, "Fallo cerrado")
