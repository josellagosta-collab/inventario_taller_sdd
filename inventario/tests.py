from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from auditoria.models import RegistroAuditoria
from incidencias.models import Incidencia
from ubicaciones.models import Aula, Edificio, Ubicacion
from usuarios.models import PerfilUsuario

from .forms import MaterialForm, TrasladoMaterialForm
from .models import Categoria, Material, MovimientoInventario, Subcategoria
from .templatetags.moneda import euros
from .views import construir_historial_material


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
