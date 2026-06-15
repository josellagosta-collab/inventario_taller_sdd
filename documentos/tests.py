import shutil
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from auditoria.models import RegistroAuditoria
from inventario.models import Categoria, Material

from .models import Documento, Fotografia


TEST_MEDIA_ROOT = settings.BASE_DIR / ".test_media_documentos"


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class DescargarDocumentoTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(Path(TEST_MEDIA_ROOT), ignore_errors=True)

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="profesor",
            password="testpass123",
        )
        self.categoria = Categoria.objects.create(nombre="Redes")
        self.material = Material.objects.create(
            codigo_inventario="DOC-001",
            nombre="Switch documentado",
            categoria=self.categoria,
            cantidad=1,
        )
        self.documento = Documento.objects.create(
            material=self.material,
            nombre="Manual",
            archivo=SimpleUploadedFile(
                "manual.txt",
                b"contenido del manual",
                content_type="text/plain",
            ),
            tipo_documento="manual",
            usuario=self.usuario,
        )

    def test_descarga_documento_requiere_login(self):
        response = self.client.get(
            reverse("documentos:descargar_documento", args=[self.documento.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_descarga_documento_autenticado_devuelve_archivo(self):
        self.client.login(username="profesor", password="testpass123")

        response = self.client.get(
            reverse("documentos:descargar_documento", args=[self.documento.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertIn(".txt", response["Content-Disposition"])

    def test_descarga_documento_registra_auditoria(self):
        self.client.login(username="profesor", password="testpass123")

        self.client.get(
            reverse("documentos:descargar_documento", args=[self.documento.id])
        )

        self.assertTrue(
            RegistroAuditoria.objects.filter(
                accion="acceder",
                descripcion__icontains="Descarga de documento",
            ).exists()
        )


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class FotografiaMaterialTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(Path(TEST_MEDIA_ROOT), ignore_errors=True)

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="admin",
            password="testpass123",
        )
        grupo = self.usuario.groups.model.objects.create(name="Administradores")
        self.usuario.groups.add(grupo)
        self.client.login(username="admin", password="testpass123")
        self.categoria = Categoria.objects.create(nombre="Robótica")
        self.material = Material.objects.create(
            codigo_inventario="FOTO-001",
            nombre="Robot con imagen",
            categoria=self.categoria,
            cantidad=1,
        )

    def imagen_valida(self):
        return SimpleUploadedFile(
            "foto.gif",
            (
                b"GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
                b"\xff\xff\xff,\x00\x00\x00\x00\x01\x00\x01\x00"
                b"\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )

    def test_subir_fotografia_crea_imagen_asociada_al_material(self):
        response = self.client.post(
            reverse("documentos:subir_fotografia", args=[self.material.id]),
            {
                "titulo": "Vista frontal",
                "descripcion": "Foto del frontal",
                "imagen": self.imagen_valida(),
            },
        )

        self.assertRedirects(
            response,
            reverse("inventario:detalle_material", args=[self.material.id]),
        )
        self.assertTrue(
            Fotografia.objects.filter(
                material=self.material,
                titulo="Vista frontal",
            ).exists()
        )

    def test_detalle_material_muestra_fotografia(self):
        Fotografia.objects.create(
            material=self.material,
            titulo="Vista lateral",
            descripcion="Foto lateral",
            imagen=self.imagen_valida(),
            usuario=self.usuario,
        )

        response = self.client.get(
            reverse("inventario:detalle_material", args=[self.material.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vista lateral")
        self.assertContains(response, "Foto lateral")
