from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from auditoria.models import RegistroAuditoria
from inventario.models import Categoria, Material
from inventario.models import MovimientoInventario
from usuarios.models import PerfilUsuario

from .forms import MantenimientoForm
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


class MantenimientoFormTests(TestCase):
    def test_formulario_valido(self):
        hoy = timezone.now().date()
        form = MantenimientoForm(data={
            "tipo": Mantenimiento.TIPO_PREVENTIVO,
            "fecha": hoy.isoformat(),
            "descripcion": "Revisión de limpieza",
            "resultado": Mantenimiento.RESULTADO_OK,
            "coste": "0.00",
            "proxima_revision": (hoy + timedelta(days=30)).isoformat(),
            "observaciones": "",
        })

        self.assertTrue(form.is_valid())

    def test_formulario_rechaza_coste_negativo(self):
        form = MantenimientoForm(data={
            "tipo": Mantenimiento.TIPO_PREVENTIVO,
            "fecha": timezone.now().date().isoformat(),
            "descripcion": "Revisión",
            "resultado": Mantenimiento.RESULTADO_OK,
            "coste": "-1.00",
            "observaciones": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("coste", form.errors)


class CrearMantenimientoMaterialTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="MANT-VIEW-001",
            nombre="Equipo con mantenimiento",
            categoria=self.categoria,
            cantidad=1,
        )
        self.usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.usuario)
        grupo = self.usuario.groups.model.objects.create(name="Administradores")
        self.usuario.groups.add(grupo)
        self.client.login(username="admin", password="testpass123")

    def test_crear_mantenimiento_desde_material(self):
        hoy = timezone.now().date()

        response = self.client.post(
            reverse(
                "mantenimiento:crear_mantenimiento_material",
                args=[self.material.id],
            ),
            {
                "tipo": Mantenimiento.TIPO_CORRECTIVO,
                "fecha": hoy.isoformat(),
                "descripcion": "Sustitución de fuente",
                "resultado": Mantenimiento.RESULTADO_REPARADO,
                "coste": "15.50",
                "proxima_revision": (hoy + timedelta(days=90)).isoformat(),
                "observaciones": "Probado correctamente",
            },
        )

        self.assertRedirects(
            response,
            reverse("inventario:detalle_material", args=[self.material.id]),
        )
        mantenimiento = Mantenimiento.objects.get(material=self.material)
        self.assertEqual(mantenimiento.tecnico, self.usuario)
        self.assertEqual(mantenimiento.tipo, Mantenimiento.TIPO_CORRECTIVO)
        self.assertTrue(MovimientoInventario.objects.filter(
            material=self.material,
            tipo="ajuste",
            descripcion__icontains="Mantenimiento registrado",
        ).exists())
        self.assertTrue(RegistroAuditoria.objects.filter(
            accion="crear",
            descripcion__icontains="Mantenimiento registrado",
        ).exists())
