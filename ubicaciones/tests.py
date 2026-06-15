from django.db import IntegrityError
from django.test import TestCase

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
