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

from .forms import MantenimientoForm, PlanMantenimientoForm
from .models import Mantenimiento, PlanMantenimiento


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


class PlanMantenimientoModelTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="PLAN-001",
            nombre="Equipo con plan",
            categoria=self.categoria,
            cantidad=1,
        )
        self.responsable = User.objects.create_user(username="responsable")

    def test_crear_plan_mantenimiento_valido(self):
        hoy = timezone.now().date()
        plan = PlanMantenimiento.objects.create(
            material=self.material,
            responsable=self.responsable,
            nombre="Revisión mensual",
            tipo=Mantenimiento.TIPO_PREVENTIVO,
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=30),
        )

        self.assertEqual(plan.material, self.material)
        self.assertEqual(plan.responsable, self.responsable)
        self.assertTrue(plan.activo)

    def test_frecuencia_debe_ser_mayor_que_cero(self):
        hoy = timezone.now().date()
        plan = PlanMantenimiento(
            material=self.material,
            responsable=self.responsable,
            nombre="Plan incorrecto",
            frecuencia_dias=0,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=30),
        )

        with self.assertRaises(ValidationError):
            plan.full_clean()

    def test_proxima_revision_no_puede_ser_anterior_a_inicio(self):
        hoy = timezone.now().date()
        plan = PlanMantenimiento(
            material=self.material,
            responsable=self.responsable,
            nombre="Plan con fecha incorrecta",
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy - timedelta(days=1),
        )

        with self.assertRaises(ValidationError):
            plan.full_clean()

    def test_estado_revision_vencido_proximo_y_al_dia(self):
        hoy = timezone.now().date()
        plan_vencido = PlanMantenimiento(
            material=self.material,
            nombre="Plan vencido",
            frecuencia_dias=30,
            fecha_inicio=hoy - timedelta(days=30),
            proxima_revision=hoy - timedelta(days=1),
        )
        plan_proximo = PlanMantenimiento(
            material=self.material,
            nombre="Plan próximo",
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=3),
        )
        plan_al_dia = PlanMantenimiento(
            material=self.material,
            nombre="Plan al día",
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=30),
        )

        self.assertEqual(plan_vencido.estado_revision, "vencido")
        self.assertEqual(plan_proximo.estado_revision, "proximo")
        self.assertEqual(plan_al_dia.estado_revision, "al_dia")


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


class PlanMantenimientoFormTests(TestCase):
    def test_formulario_plan_valido(self):
        hoy = timezone.now().date()
        form = PlanMantenimientoForm(data={
            "nombre": "Revisión trimestral",
            "tipo": Mantenimiento.TIPO_PREVENTIVO,
            "descripcion": "Comprobación preventiva",
            "frecuencia_dias": "90",
            "fecha_inicio": hoy.isoformat(),
            "proxima_revision": (hoy + timedelta(days=90)).isoformat(),
            "activo": "on",
            "observaciones": "",
        })

        self.assertTrue(form.is_valid())

    def test_formulario_plan_rechaza_frecuencia_cero(self):
        hoy = timezone.now().date()
        form = PlanMantenimientoForm(data={
            "nombre": "Plan incorrecto",
            "tipo": Mantenimiento.TIPO_PREVENTIVO,
            "descripcion": "",
            "frecuencia_dias": "0",
            "fecha_inicio": hoy.isoformat(),
            "proxima_revision": (hoy + timedelta(days=30)).isoformat(),
            "activo": "on",
            "observaciones": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("frecuencia_dias", form.errors)


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


class HistoricoMantenimientoTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="HIST-MANT-001",
            nombre="Equipo con histórico",
            categoria=self.categoria,
            cantidad=1,
        )
        self.otro_material = Material.objects.create(
            codigo_inventario="HIST-MANT-002",
            nombre="Equipo auxiliar",
            categoria=self.categoria,
            cantidad=1,
        )
        self.usuario = User.objects.create_user(
            username="tecnico_historial",
            password="testpass123",
        )
        self.client.login(username="tecnico_historial", password="testpass123")

    def test_lista_mantenimientos_filtra_por_material(self):
        hoy = timezone.now().date()
        Mantenimiento.objects.create(
            material=self.material,
            tecnico=self.usuario,
            tipo=Mantenimiento.TIPO_PREVENTIVO,
            fecha=hoy,
            descripcion="Revisión visible",
            resultado=Mantenimiento.RESULTADO_OK,
            coste=0,
        )
        Mantenimiento.objects.create(
            material=self.otro_material,
            tecnico=self.usuario,
            tipo=Mantenimiento.TIPO_CORRECTIVO,
            fecha=hoy,
            descripcion="Revisión oculta",
            resultado=Mantenimiento.RESULTADO_REPARADO,
            coste=10,
        )

        response = self.client.get(
            reverse("mantenimiento:lista_mantenimientos"),
            {"busqueda": "HIST-MANT-001"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Revisión visible")
        self.assertNotContains(response, "Revisión oculta")

    def test_detalle_material_muestra_historico_de_mantenimiento(self):
        Mantenimiento.objects.create(
            material=self.material,
            tecnico=self.usuario,
            tipo=Mantenimiento.TIPO_CORRECTIVO,
            fecha=timezone.now().date(),
            descripcion="Cambio de componente",
            resultado=Mantenimiento.RESULTADO_REPARADO,
            coste=25,
        )

        response = self.client.get(
            reverse("inventario:detalle_material", args=[self.material.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Histórico de mantenimiento")
        self.assertContains(response, "Cambio de componente")
        self.assertContains(response, "Mantenimiento")


class PlanificacionMantenimientoTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="PLAN-VIEW-001",
            nombre="Equipo planificado",
            categoria=self.categoria,
            cantidad=1,
        )
        self.otro_material = Material.objects.create(
            codigo_inventario="PLAN-VIEW-002",
            nombre="Equipo sin filtrar",
            categoria=self.categoria,
            cantidad=1,
        )
        self.usuario = User.objects.create_user(
            username="admin_plan",
            password="testpass123",
        )
        PerfilUsuario.objects.get_or_create(user=self.usuario)
        grupo = self.usuario.groups.model.objects.create(name="Administradores")
        self.usuario.groups.add(grupo)
        self.client.login(username="admin_plan", password="testpass123")

    def test_crear_plan_desde_material(self):
        hoy = timezone.now().date()

        response = self.client.post(
            reverse(
                "mantenimiento:crear_plan_mantenimiento_material",
                args=[self.material.id],
            ),
            {
                "nombre": "Revisión mensual",
                "tipo": Mantenimiento.TIPO_PREVENTIVO,
                "descripcion": "Limpieza y comprobación",
                "frecuencia_dias": "30",
                "fecha_inicio": hoy.isoformat(),
                "proxima_revision": (hoy + timedelta(days=30)).isoformat(),
                "activo": "on",
                "observaciones": "Plan inicial",
            },
        )

        self.assertRedirects(
            response,
            reverse("inventario:detalle_material", args=[self.material.id]),
        )
        plan = PlanMantenimiento.objects.get(material=self.material)
        self.assertEqual(plan.responsable, self.usuario)
        self.assertEqual(plan.nombre, "Revisión mensual")
        self.assertTrue(RegistroAuditoria.objects.filter(
            accion="crear",
            descripcion__icontains="Plan de mantenimiento creado",
        ).exists())

    def test_lista_planes_filtra_por_material(self):
        hoy = timezone.now().date()
        PlanMantenimiento.objects.create(
            material=self.material,
            responsable=self.usuario,
            nombre="Plan visible",
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=30),
        )
        PlanMantenimiento.objects.create(
            material=self.otro_material,
            responsable=self.usuario,
            nombre="Plan oculto",
            frecuencia_dias=60,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=60),
        )

        response = self.client.get(
            reverse("mantenimiento:lista_planes_mantenimiento"),
            {"busqueda": "PLAN-VIEW-001"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Plan visible")
        self.assertNotContains(response, "Plan oculto")

    def test_lista_planes_filtra_alertas_vencidas(self):
        hoy = timezone.now().date()
        PlanMantenimiento.objects.create(
            material=self.material,
            responsable=self.usuario,
            nombre="Plan vencido",
            frecuencia_dias=30,
            fecha_inicio=hoy - timedelta(days=30),
            proxima_revision=hoy - timedelta(days=1),
        )
        PlanMantenimiento.objects.create(
            material=self.otro_material,
            responsable=self.usuario,
            nombre="Plan futuro",
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=30),
        )

        response = self.client.get(
            reverse("mantenimiento:lista_planes_mantenimiento"),
            {"alerta": "vencidos"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Plan vencido")
        self.assertContains(response, "Revisión vencida")
        self.assertNotContains(response, "Plan futuro")

    def test_dashboard_muestra_contadores_de_revision(self):
        hoy = timezone.now().date()
        PlanMantenimiento.objects.create(
            material=self.material,
            responsable=self.usuario,
            nombre="Plan vencido",
            frecuencia_dias=30,
            fecha_inicio=hoy - timedelta(days=30),
            proxima_revision=hoy - timedelta(days=1),
        )
        PlanMantenimiento.objects.create(
            material=self.otro_material,
            responsable=self.usuario,
            nombre="Plan próximo",
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=3),
        )

        response = self.client.get(reverse("inventario:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Revisiones vencidas")
        self.assertContains(response, "Revisiones próximas")

    def test_detalle_material_muestra_planes(self):
        hoy = timezone.now().date()
        PlanMantenimiento.objects.create(
            material=self.material,
            responsable=self.usuario,
            nombre="Plan en detalle",
            frecuencia_dias=30,
            fecha_inicio=hoy,
            proxima_revision=hoy + timedelta(days=30),
        )

        response = self.client.get(
            reverse("inventario:detalle_material", args=[self.material.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Planes de mantenimiento")
        self.assertContains(response, "Plan en detalle")
