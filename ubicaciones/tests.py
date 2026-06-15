from django.db import IntegrityError
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from auditoria.models import RegistroAuditoria
from .forms import UbicacionForm
from .models import Armario, Aula, Caja, Edificio, Estanteria, Ubicacion


class UbicacionesModelTests(TestCase):
    def setUp(self):
        self.edificio = Edificio.objects.create(nombre="Edificio A")
        self.aula = Aula.objects.create(
            edificio=self.edificio,
            nombre="Aula 1",
        )
        self.armario = Armario.objects.create(
            aula=self.aula,
            nombre="Armario 1",
        )
        self.estanteria = Estanteria.objects.create(
            armario=self.armario,
            nombre="Estantería 1",
        )
        self.caja = Caja.objects.create(
            estanteria=self.estanteria,
            nombre="Caja 1",
        )

    def test_ubicacion_construye_ruta_legible(self):
        ubicacion = Ubicacion.objects.create(
            edificio=self.edificio,
            aula=self.aula,
            armario=self.armario,
            estanteria=self.estanteria,
            caja=self.caja,
            posicion="Bandeja superior",
        )

        self.assertEqual(
            str(ubicacion),
            "Edificio A / Aula 1 / Armario 1 / Estantería 1 / Caja 1 / Bandeja superior",
        )

    def test_no_permite_aulas_duplicadas_en_el_mismo_edificio(self):
        with self.assertRaises(IntegrityError):
            Aula.objects.create(
                edificio=self.edificio,
                nombre="Aula 1",
            )

    def test_modelos_intermedios_devuelven_jerarquia(self):
        self.assertEqual(str(self.aula), "Edificio A - Aula 1")
        self.assertEqual(str(self.armario), "Edificio A - Aula 1 - Armario 1")
        self.assertEqual(
            str(self.estanteria),
            "Edificio A - Aula 1 - Armario 1 - Estantería 1",
        )
        self.assertEqual(
            str(self.caja),
            "Edificio A - Aula 1 - Armario 1 - Estantería 1 - Caja 1",
        )


class UbicacionFormTests(TestCase):
    def setUp(self):
        self.edificio = Edificio.objects.create(nombre="Edificio A")
        self.otro_edificio = Edificio.objects.create(nombre="Edificio B")
        self.aula = Aula.objects.create(
            edificio=self.edificio,
            nombre="Aula 1",
        )
        self.aula_otro_edificio = Aula.objects.create(
            edificio=self.otro_edificio,
            nombre="Aula 2",
        )
        self.armario = Armario.objects.create(
            aula=self.aula,
            nombre="Armario 1",
        )
        self.estanteria = Estanteria.objects.create(
            armario=self.armario,
            nombre="Estantería 1",
        )
        self.caja = Caja.objects.create(
            estanteria=self.estanteria,
            nombre="Caja 1",
        )

    def test_formulario_valido_con_jerarquia_completa(self):
        form = UbicacionForm(data={
            "edificio": self.edificio.id,
            "aula": self.aula.id,
            "armario": self.armario.id,
            "estanteria": self.estanteria.id,
            "caja": self.caja.id,
            "posicion": "Bandeja superior",
            "descripcion": "",
        })

        self.assertTrue(form.is_valid())

    def test_rechaza_aula_de_otro_edificio(self):
        form = UbicacionForm(data={
            "edificio": self.edificio.id,
            "aula": self.aula_otro_edificio.id,
            "armario": "",
            "estanteria": "",
            "caja": "",
            "posicion": "",
            "descripcion": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("aula", form.errors)

    def test_rechaza_armario_sin_aula(self):
        form = UbicacionForm(data={
            "edificio": self.edificio.id,
            "aula": "",
            "armario": self.armario.id,
            "estanteria": "",
            "caja": "",
            "posicion": "",
            "descripcion": "",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("armario", form.errors)


class UbicacionesViewTests(TestCase):
    def setUp(self):
        self.grupo_admin = Group.objects.create(name="Administradores")
        self.usuario = User.objects.create_user(
            username="admin_ubicaciones",
            password="testpass123",
        )
        self.usuario.groups.add(self.grupo_admin)
        self.client.login(username="admin_ubicaciones", password="testpass123")

        self.edificio_a = Edificio.objects.create(nombre="Edificio A")
        self.edificio_b = Edificio.objects.create(nombre="Edificio B")
        self.aula_a = Aula.objects.create(
            edificio=self.edificio_a,
            nombre="Aula Hardware",
        )
        self.aula_b = Aula.objects.create(
            edificio=self.edificio_b,
            nombre="Aula Redes",
        )
        self.ubicacion_visible = Ubicacion.objects.create(
            edificio=self.edificio_a,
            aula=self.aula_a,
            posicion="Armario visible",
        )
        self.ubicacion_oculta = Ubicacion.objects.create(
            edificio=self.edificio_b,
            aula=self.aula_b,
            posicion="Armario oculto",
        )

    def test_lista_ubicaciones_filtra_por_busqueda(self):
        response = self.client.get(
            reverse("ubicaciones:lista_ubicaciones"),
            {"busqueda": "visible"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Armario visible")
        self.assertNotContains(response, "Armario oculto")

    def test_crear_ubicacion_registra_auditoria(self):
        response = self.client.post(
            reverse("ubicaciones:crear_ubicacion"),
            {
                "edificio": self.edificio_a.id,
                "aula": self.aula_a.id,
                "armario": "",
                "estanteria": "",
                "caja": "",
                "posicion": "Mesa de pruebas",
                "descripcion": "",
            },
        )

        self.assertRedirects(response, reverse("ubicaciones:lista_ubicaciones"))
        self.assertTrue(
            Ubicacion.objects.filter(posicion="Mesa de pruebas").exists()
        )
        self.assertTrue(
            RegistroAuditoria.objects.filter(
                accion="crear",
                descripcion__icontains="Creación de ubicación",
            ).exists()
        )

    def test_eliminar_ubicacion_por_get_muestra_confirmacion(self):
        response = self.client.get(
            reverse(
                "ubicaciones:eliminar_ubicacion",
                args=[self.ubicacion_oculta.id],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Armario oculto")
