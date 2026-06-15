import shutil
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from auditoria.models import RegistroAuditoria
from inventario.models import Categoria, Material

from .models import Documento


TEST_MEDIA_ROOT = settings.BASE_DIR / "tmp_test_media"


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
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="manual.txt"')

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
