from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from incidencias.models import Incidencia

from .forms import MaterialForm
from .models import Categoria, Material, MovimientoInventario, Subcategoria
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
