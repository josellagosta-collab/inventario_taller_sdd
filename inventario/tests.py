from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .forms import MaterialForm
from .models import Categoria, Material, Subcategoria


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
