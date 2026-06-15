from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.db import connection
from django.db import IntegrityError
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from auditoria.models import RegistroAuditoria
from incidencias.models import Incidencia
from prestamos.models import LineaPrestamo, Prestamo, Reserva
from ubicaciones.models import Aula, Edificio, Ubicacion
from usuarios.models import PerfilUsuario

from .forms import MaterialForm, TrasladoMaterialForm
from .models import Categoria, Material, MovimientoInventario, Subcategoria
from .templatetags.moneda import euros
from .views import construir_historial_material


class InventarioModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Componentes")
        self.subcategoria = Subcategoria.objects.create(
            categoria=self.categoria,
            nombre="CPU",
        )
        self.material = Material.objects.create(
            codigo_inventario="INV-001",
            nombre="Procesador de pruebas",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            cantidad=1,
        )

    def test_categoria_subcategoria_y_material_devuelven_texto_legible(self):
        self.assertEqual(str(self.categoria), "Componentes")
        self.assertEqual(str(self.subcategoria), "Componentes - CPU")
        self.assertEqual(str(self.material), "INV-001 - Procesador de pruebas")

    def test_subcategoria_no_se_repite_en_la_misma_categoria(self):
        with self.assertRaises(IntegrityError):
            Subcategoria.objects.create(
                categoria=self.categoria,
                nombre="CPU",
            )

    def test_movimiento_inventario_devuelve_material_y_tipo(self):
        movimiento = MovimientoInventario.objects.create(
            material=self.material,
            tipo="alta",
            descripcion="Alta inicial",
        )

        self.assertEqual(str(movimiento), "Procesador de pruebas - Alta")


class MaterialFormValidacionesTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Componentes")
        self.subcategoria = Subcategoria.objects.create(
            categoria=self.categoria,
            nombre="CPU",
        )

    def datos_validos(self, **overrides):
        datos = {
            "codigo_inventario": "MAT-001",
            "nombre": "Procesador Intel",
            "descripcion": "",
            "categoria": self.categoria.id,
            "subcategoria": self.subcategoria.id,
            "proveedor": "",
            "marca": "Intel",
            "modelo": "i5",
            "numero_serie": "SN-001",
            "cantidad": 1,
            "stock_minimo": 0,
            "precio_compra": "120.00",
            "fecha_compra": timezone.now().date().isoformat(),
            "garantia_hasta": (timezone.now().date() + timedelta(days=365)).isoformat(),
            "estado": "disponible",
            "ubicacion": "",
            "observaciones": "",
        }
        datos.update(overrides)
        return datos

    def test_rechaza_codigo_inventario_duplicado_sin_importar_mayusculas(self):
        Material.objects.create(
            codigo_inventario="MAT-001",
            nombre="Material existente",
            categoria=self.categoria,
            cantidad=1,
        )

        form = MaterialForm(data=self.datos_validos(codigo_inventario="mat-001"))

        self.assertFalse(form.is_valid())
        self.assertIn("codigo_inventario", form.errors)

    def test_rechaza_fecha_compra_futura(self):
        form = MaterialForm(data=self.datos_validos(
            fecha_compra=(timezone.now().date() + timedelta(days=1)).isoformat(),
        ))

        self.assertFalse(form.is_valid())
        self.assertIn("fecha_compra", form.errors)

    def test_rechaza_precio_negativo(self):
        form = MaterialForm(data=self.datos_validos(precio_compra="-1.00"))

        self.assertFalse(form.is_valid())
        self.assertIn("precio_compra", form.errors)

    def test_rechaza_cantidad_cero_para_material_disponible(self):
        form = MaterialForm(data=self.datos_validos(cantidad=0))

        self.assertFalse(form.is_valid())
        self.assertIn("cantidad", form.errors)


class FormatoMonedaTests(TestCase):
    def test_formatea_importes_en_euros_con_punto_de_millar(self):
        self.assertEqual(euros("1234.5"), "1.234,50 €")
        self.assertEqual(euros("1234567.89"), "1.234.567,89 €")

    def test_formatea_importes_vacios_como_guion(self):
        self.assertEqual(euros(None), "-")
        self.assertEqual(euros(""), "-")


class HistorialMaterialTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="admin")
        self.categoria = Categoria.objects.create(nombre="Componentes")
        self.material = Material.objects.create(
            codigo_inventario="MAT-HIST-001",
            nombre="Router de pruebas",
            categoria=self.categoria,
            cantidad=1,
        )

    def test_historial_material_incluye_movimientos_e_incidencias(self):
        MovimientoInventario.objects.create(
            material=self.material,
            tipo="alta",
            usuario=self.usuario,
            descripcion="Alta inicial",
        )
        Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="No arranca",
            descripcion="El equipo no arranca",
            prioridad="alta",
        )

        historial = construir_historial_material(self.material)
        tipos = [evento["tipo"] for evento in historial]

        self.assertIn("Movimiento", tipos)
        self.assertIn("Incidencia", tipos)

    def test_historial_material_ordena_por_fecha_descendente(self):
        antiguo = MovimientoInventario.objects.create(
            material=self.material,
            tipo="alta",
            usuario=self.usuario,
            descripcion="Alta inicial",
        )
        reciente = MovimientoInventario.objects.create(
            material=self.material,
            tipo="edicion",
            usuario=self.usuario,
            descripcion="Edición posterior",
        )
        MovimientoInventario.objects.filter(pk=antiguo.pk).update(
            fecha=timezone.now() - timedelta(days=2)
        )
        MovimientoInventario.objects.filter(pk=reciente.pk).update(
            fecha=timezone.now()
        )

        historial = construir_historial_material(self.material)

        self.assertEqual(historial[0]["titulo"], "Edición")


class AuditoriaEdicionMaterialTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.usuario)
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin", password="testpass123")
        self.categoria = Categoria.objects.create(nombre="Componentes")
        self.subcategoria = Subcategoria.objects.create(
            categoria=self.categoria,
            nombre="Router",
        )
        self.material = Material.objects.create(
            codigo_inventario="MAT-AUD-001",
            nombre="Router antiguo",
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            cantidad=1,
            stock_minimo=0,
            estado="disponible",
        )

    def datos_material(self, **overrides):
        datos = {
            "codigo_inventario": self.material.codigo_inventario,
            "nombre": self.material.nombre,
            "descripcion": self.material.descripcion or "",
            "categoria": self.categoria.id,
            "subcategoria": self.subcategoria.id,
            "proveedor": "",
            "marca": self.material.marca or "",
            "modelo": self.material.modelo or "",
            "numero_serie": self.material.numero_serie or "",
            "cantidad": self.material.cantidad,
            "stock_minimo": self.material.stock_minimo,
            "precio_compra": self.material.precio_compra or "",
            "fecha_compra": self.material.fecha_compra or "",
            "garantia_hasta": self.material.garantia_hasta or "",
            "estado": self.material.estado,
            "ubicacion": "",
            "observaciones": self.material.observaciones or "",
        }
        datos.update(overrides)
        return datos

    def test_editar_material_registra_auditoria_con_cambios(self):
        response = self.client.post(
            reverse("inventario:editar_material", args=[self.material.id]),
            self.datos_material(nombre="Router nuevo", cantidad=2),
        )

        self.assertRedirects(
            response,
            reverse("inventario:detalle_material", args=[self.material.id]),
        )
        auditoria = RegistroAuditoria.objects.get(accion="editar")
        movimiento = MovimientoInventario.objects.get(tipo="edicion")
        self.assertIn("Material editado. Cambios:", auditoria.descripcion)
        self.assertIn("nombre: Router antiguo -> Router nuevo", auditoria.descripcion)
        self.assertIn("cantidad: 1 -> 2", auditoria.descripcion)
        self.assertEqual(movimiento.descripcion, auditoria.descripcion)

    def test_editar_material_sin_cambios_no_registra_auditoria(self):
        response = self.client.post(
            reverse("inventario:editar_material", args=[self.material.id]),
            self.datos_material(),
        )

        self.assertRedirects(
            response,
            reverse("inventario:detalle_material", args=[self.material.id]),
        )
        self.assertFalse(RegistroAuditoria.objects.filter(accion="editar").exists())
        self.assertFalse(MovimientoInventario.objects.filter(tipo="edicion").exists())


class TrasladoMaterialTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.usuario)
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin", password="testpass123")

        self.categoria = Categoria.objects.create(nombre="Componentes")
        self.edificio = Edificio.objects.create(nombre="Edificio A")
        self.aula_origen = Aula.objects.create(
            edificio=self.edificio,
            nombre="Aula 1",
        )
        self.aula_destino = Aula.objects.create(
            edificio=self.edificio,
            nombre="Aula 2",
        )
        self.ubicacion_origen = Ubicacion.objects.create(
            edificio=self.edificio,
            aula=self.aula_origen,
            posicion="Armario origen",
        )
        self.ubicacion_destino = Ubicacion.objects.create(
            edificio=self.edificio,
            aula=self.aula_destino,
            posicion="Armario destino",
        )
        self.material = Material.objects.create(
            codigo_inventario="MAT-TRAS-001",
            nombre="Switch de pruebas",
            categoria=self.categoria,
            cantidad=1,
            ubicacion=self.ubicacion_origen,
        )

    def test_formulario_rechaza_misma_ubicacion(self):
        form = TrasladoMaterialForm(
            data={"ubicacion": self.ubicacion_origen.id},
            material=self.material,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("ubicacion", form.errors)

    def test_trasladar_material_actualiza_ubicacion_y_registra_movimiento(self):
        response = self.client.post(
            reverse("inventario:trasladar_material", args=[self.material.id]),
            {
                "ubicacion": self.ubicacion_destino.id,
                "observaciones": "Cambio por reorganización del taller",
            },
        )

        self.assertRedirects(
            response,
            reverse("inventario:detalle_material", args=[self.material.id]),
        )
        self.material.refresh_from_db()
        self.assertEqual(self.material.ubicacion, self.ubicacion_destino)

        movimiento = MovimientoInventario.objects.get(tipo="traslado")
        self.assertIn("Origen:", movimiento.descripcion)
        self.assertIn("Destino:", movimiento.descripcion)
        self.assertIn("Cambio por reorganización", movimiento.descripcion)

        auditoria = RegistroAuditoria.objects.get(accion="editar")
        self.assertEqual(auditoria.descripcion, movimiento.descripcion)


class FlujosIntegracionTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.admin = User.objects.create_user(
            username="admin_integracion",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.admin)
        self.admin.groups.add(self.grupo_admin)
        self.alumno = User.objects.create_user(username="alumno_integracion")
        self.client.login(username="admin_integracion", password="testpass123")

        self.categoria = Categoria.objects.create(nombre="Integración")
        self.material = Material.objects.create(
            codigo_inventario="INT-001",
            nombre="Material integrado",
            categoria=self.categoria,
            cantidad=1,
            estado="disponible",
        )

    def test_flujo_prestamo_y_devolucion_actualiza_inventario_movimientos_y_auditoria(self):
        response = self.client.post(
            reverse("prestamos:crear_prestamo"),
            {
                "usuario_receptor": self.alumno.id,
                "profesor_responsable": self.admin.id,
                "fecha_prevista_devolucion": (
                    timezone.now().date() + timedelta(days=7)
                ).isoformat(),
                "observaciones": "Préstamo de integración",
                "material": self.material.id,
                "cantidad": 1,
            },
        )

        self.assertRedirects(response, reverse("prestamos:lista_prestamos"))
        prestamo = Prestamo.objects.get(usuario_receptor=self.alumno)
        self.material.refresh_from_db()

        self.assertEqual(self.material.estado, "prestado")
        self.assertTrue(
            LineaPrestamo.objects.filter(
                prestamo=prestamo,
                material=self.material,
                cantidad=1,
            ).exists()
        )
        self.assertTrue(
            MovimientoInventario.objects.filter(
                material=self.material,
                tipo="prestamo",
            ).exists()
        )
        self.assertTrue(
            RegistroAuditoria.objects.filter(
                accion="prestar",
                descripcion__icontains=f"Préstamo ID: {prestamo.id}",
            ).exists()
        )

        response = self.client.post(
            reverse("prestamos:devolver_prestamo", args=[prestamo.id])
        )

        self.assertRedirects(response, reverse("prestamos:lista_prestamos"))
        prestamo.refresh_from_db()
        self.material.refresh_from_db()

        self.assertEqual(prestamo.estado, "devuelto")
        self.assertEqual(self.material.estado, "disponible")
        self.assertTrue(
            MovimientoInventario.objects.filter(
                material=self.material,
                tipo="devolucion",
            ).exists()
        )
        self.assertTrue(
            RegistroAuditoria.objects.filter(
                accion="devolver",
                descripcion__icontains=f"Préstamo ID: {prestamo.id}",
            ).exists()
        )

    def test_flujo_reserva_y_conversion_en_prestamo(self):
        response = self.client.post(
            reverse("prestamos:crear_reserva"),
            {
                "usuario_reserva": self.alumno.id,
                "profesor_responsable": self.admin.id,
                "material": self.material.id,
                "cantidad": 1,
                "fecha_prevista_recogida": (
                    timezone.now().date() + timedelta(days=3)
                ).isoformat(),
                "observaciones": "Reserva de integración",
            },
        )

        self.assertRedirects(response, reverse("prestamos:lista_reservas"))
        reserva = Reserva.objects.get(usuario_reserva=self.alumno)
        self.material.refresh_from_db()

        self.assertEqual(reserva.estado, "activa")
        self.assertEqual(self.material.estado, "reservado")
        self.assertTrue(
            RegistroAuditoria.objects.filter(
                accion="reservar",
                descripcion__icontains=f"Reserva ID: {reserva.id}",
            ).exists()
        )

        response = self.client.post(
            reverse("prestamos:convertir_reserva_en_prestamo", args=[reserva.id])
        )

        prestamo = Prestamo.objects.get(usuario_receptor=self.alumno)
        self.assertRedirects(
            response,
            reverse("prestamos:detalle_prestamo", args=[prestamo.id]),
        )
        reserva.refresh_from_db()
        self.material.refresh_from_db()

        self.assertEqual(reserva.estado, "convertida")
        self.assertEqual(self.material.estado, "prestado")
        self.assertTrue(
            LineaPrestamo.objects.filter(
                prestamo=prestamo,
                material=self.material,
            ).exists()
        )
        self.assertTrue(
            RegistroAuditoria.objects.filter(
                accion="convertir_reserva",
                descripcion__icontains=f"Reserva ID: {reserva.id}",
            ).exists()
        )

    def test_flujo_incidencia_y_resolucion_actualiza_estado_y_movimientos(self):
        response = self.client.post(
            reverse("incidencias:crear_incidencia", args=[self.material.id]),
            {
                "titulo": "Fallo integrado",
                "descripcion": "El material falla durante la prueba.",
                "prioridad": "alta",
            },
        )

        self.assertRedirects(
            response,
            reverse("inventario:detalle_material", args=[self.material.id]),
        )
        incidencia = Incidencia.objects.get(titulo="Fallo integrado")
        self.material.refresh_from_db()

        self.assertEqual(self.material.estado, "averiado")
        self.assertTrue(
            MovimientoInventario.objects.filter(
                material=self.material,
                descripcion__icontains="Incidencia creada",
            ).exists()
        )

        response = self.client.post(
            reverse("incidencias:resolver_incidencia", args=[incidencia.id]),
            {
                "solucion": "Se sustituye el componente defectuoso.",
            },
        )

        self.assertRedirects(
            response,
            reverse("incidencias:detalle_incidencia", args=[incidencia.id]),
        )
        incidencia.refresh_from_db()
        self.material.refresh_from_db()

        self.assertEqual(incidencia.estado, "cerrada")
        self.assertEqual(self.material.estado, "disponible")
        self.assertTrue(
            MovimientoInventario.objects.filter(
                material=self.material,
                descripcion__icontains="Incidencia resuelta",
            ).exists()
        )


class RendimientoInventarioTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username="usuario_rendimiento",
            password="testpass123",
        )
        self.client.force_login(self.usuario)
        self.categoria = Categoria.objects.create(nombre="Rendimiento")
        self.materiales = [
            Material.objects.create(
                codigo_inventario=f"PERF-{indice:03d}",
                nombre=f"Material rendimiento {indice}",
                categoria=self.categoria,
                cantidad=1,
                stock_minimo=0,
            )
            for indice in range(30)
        ]

    def assert_consultas_maximas(self, maximo, callback):
        with CaptureQueriesContext(connection) as contexto:
            response = callback()

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(
            len(contexto),
            maximo,
            f"Se ejecutaron {len(contexto)} consultas, máximo esperado {maximo}.",
        )

    def test_lista_materiales_mantiene_consultas_acotadas_con_muchos_registros(self):
        for indice, material in enumerate(self.materiales[:15]):
            Reserva.objects.create(
                usuario_reserva=self.usuario,
                profesor_responsable=self.usuario,
                material=material,
                cantidad=1,
                fecha_prevista_recogida=timezone.now().date() + timedelta(days=1),
                estado="activa" if indice % 2 == 0 else "cancelada",
            )

        self.assert_consultas_maximas(
            12,
            lambda: self.client.get(reverse("inventario:lista_materiales")),
        )

    def test_dashboard_mantiene_consultas_acotadas_con_actividad(self):
        for material in self.materiales[:10]:
            MovimientoInventario.objects.create(
                material=material,
                tipo="alta",
                usuario=self.usuario,
                descripcion="Alta de rendimiento",
            )
            Incidencia.objects.create(
                material=material,
                usuario=self.usuario,
                titulo=f"Incidencia {material.codigo_inventario}",
                descripcion="Incidencia de rendimiento",
            )

        self.assert_consultas_maximas(
            35,
            lambda: self.client.get(reverse("inventario:dashboard")),
        )
