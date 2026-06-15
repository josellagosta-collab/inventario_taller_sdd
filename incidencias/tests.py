from django.contrib.auth.models import User
from django.test import TestCase

from inventario.models import Categoria, Material

from .models import ComentarioIncidencia, Incidencia


class IncidenciasModelTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username="tecnico")
        self.categoria = Categoria.objects.create(nombre="Equipos")
        self.material = Material.objects.create(
            codigo_inventario="INC-001",
            nombre="Equipo averiado",
            categoria=self.categoria,
            cantidad=1,
        )

    def test_incidencia_tiene_estado_y_prioridad_por_defecto(self):
        incidencia = Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="No arranca",
            descripcion="El equipo no enciende",
        )

        self.assertEqual(incidencia.estado, "abierta")
        self.assertEqual(incidencia.prioridad, "media")
        self.assertEqual(str(incidencia), "No arranca - Equipo averiado")

    def test_comentario_incidencia_devuelve_titulo_de_incidencia(self):
        incidencia = Incidencia.objects.create(
            material=self.material,
            usuario=self.usuario,
            titulo="Pantalla rota",
            descripcion="Cristal dañado",
        )
        comentario = ComentarioIncidencia.objects.create(
            incidencia=incidencia,
            usuario=self.usuario,
            comentario="Pendiente de repuesto",
        )

        self.assertEqual(str(comentario), "Comentario en Pantalla rota")
        self.assertEqual(incidencia.comentarios.count(), 1)
