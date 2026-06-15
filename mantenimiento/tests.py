from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from inventario.models import Categoria, Material

from .models import Mantenimiento


class MantenimientoModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="MANT-001",
            nombre="Equipo de pruebas",
            categoria=self.categoria,
            cantidad=1,
        )
        self.tecnico = User.objects.create_user(username="tecnico")

    def test_crear_mantenimiento_valido(self):
        mantenimiento = Mantenimiento.objects.create(
            material=self.material,
            tecnico=self.tecnico,
            tipo=Mantenimiento.TIPO_PREVENTIVO,
            fecha=timezone.now().date(),
            descripcion="Revisión general",
            resultado=Mantenimiento.RESULTADO_OK,
            coste=0,
        )

        self.assertEqual(mantenimiento.material, self.material)
        self.assertEqual(mantenimiento.tecnico, self.tecnico)

    def test_coste_no_puede_ser_negativo(self):
        mantenimiento = Mantenimiento(
            material=self.material,
            tecnico=self.tecnico,
            fecha=timezone.now().date(),
            descripcion="Revisión con coste incorrecto",
            coste=-1,
        )

        with self.assertRaises(ValidationError):
            mantenimiento.full_clean()

    def test_fecha_no_puede_ser_futura(self):
        mantenimiento = Mantenimiento(
            material=self.material,
            tecnico=self.tecnico,
            fecha=timezone.now().date() + timedelta(days=1),
            descripcion="Revisión futura",
            coste=0,
        )

        with self.assertRaises(ValidationError):
            mantenimiento.full_clean()

    def test_proxima_revision_no_puede_ser_anterior(self):
        hoy = timezone.now().date()
        mantenimiento = Mantenimiento(
            material=self.material,
            tecnico=self.tecnico,
            fecha=hoy,
            proxima_revision=hoy - timedelta(days=1),
            descripcion="Revisión con próxima fecha incorrecta",
            coste=0,
        )

        with self.assertRaises(ValidationError):
            mantenimiento.full_clean()
