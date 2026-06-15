from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand, CommandError


GRUPOS_BASE = {
    "Administradores": {
        "descripcion": "Acceso completo a la aplicación.",
        "permisos": "__all__",
    },
    "Profesores": {
        "descripcion": "Consulta de inventario y gestión operativa de préstamos, reservas e incidencias.",
        "permisos": [
            ("inventario", "view_categoria"),
            ("inventario", "view_subcategoria"),
            ("inventario", "view_proveedor"),
            ("inventario", "view_material"),
            ("inventario", "view_movimientoinventario"),
            ("ubicaciones", "view_edificio"),
            ("ubicaciones", "view_aula"),
            ("ubicaciones", "view_armario"),
            ("ubicaciones", "view_estanteria"),
            ("ubicaciones", "view_caja"),
            ("ubicaciones", "view_ubicacion"),
            ("prestamos", "add_prestamo"),
            ("prestamos", "change_prestamo"),
            ("prestamos", "view_prestamo"),
            ("prestamos", "add_lineaprestamo"),
            ("prestamos", "change_lineaprestamo"),
            ("prestamos", "view_lineaprestamo"),
            ("prestamos", "add_reserva"),
            ("prestamos", "change_reserva"),
            ("prestamos", "view_reserva"),
            ("incidencias", "add_incidencia"),
            ("incidencias", "view_incidencia"),
            ("incidencias", "add_comentarioincidencia"),
            ("incidencias", "view_comentarioincidencia"),
            ("documentos", "view_documento"),
            ("documentos", "view_fotografia"),
            ("mantenimiento", "view_mantenimiento"),
            ("mantenimiento", "view_planmantenimiento"),
        ],
    },
    "Técnicos": {
        "descripcion": "Gestión técnica de incidencias, mantenimientos y revisiones.",
        "permisos": [
            ("inventario", "view_categoria"),
            ("inventario", "view_subcategoria"),
            ("inventario", "view_material"),
            ("inventario", "view_movimientoinventario"),
            ("ubicaciones", "view_ubicacion"),
            ("incidencias", "add_incidencia"),
            ("incidencias", "change_incidencia"),
            ("incidencias", "view_incidencia"),
            ("incidencias", "add_comentarioincidencia"),
            ("incidencias", "change_comentarioincidencia"),
            ("incidencias", "view_comentarioincidencia"),
            ("mantenimiento", "add_mantenimiento"),
            ("mantenimiento", "change_mantenimiento"),
            ("mantenimiento", "view_mantenimiento"),
            ("mantenimiento", "add_planmantenimiento"),
            ("mantenimiento", "change_planmantenimiento"),
            ("mantenimiento", "view_planmantenimiento"),
            ("documentos", "view_documento"),
            ("documentos", "view_fotografia"),
        ],
    },
    "Alumnos": {
        "descripcion": "Consulta básica del material y seguimiento de préstamos o reservas propios.",
        "permisos": [
            ("inventario", "view_categoria"),
            ("inventario", "view_subcategoria"),
            ("inventario", "view_material"),
            ("ubicaciones", "view_ubicacion"),
            ("prestamos", "view_prestamo"),
            ("prestamos", "view_lineaprestamo"),
            ("prestamos", "view_reserva"),
        ],
    },
}


class Command(BaseCommand):
    help = "Crea los grupos base de la aplicación, configura permisos y permite asignar usuarios."

    def add_arguments(self, parser):
        parser.add_argument(
            "--admin-user",
            action="append",
            default=[],
            help="Username que se añadirá al grupo Administradores. Se puede usar varias veces.",
        )

    def handle(self, *args, **options):
        grupos = {}

        for nombre_grupo, configuracion in GRUPOS_BASE.items():
            grupo, creado = Group.objects.get_or_create(name=nombre_grupo)
            grupos[nombre_grupo] = grupo

            permisos = self.obtener_permisos(configuracion["permisos"])
            grupo.permissions.set(permisos)

            if creado:
                self.stdout.write(self.style.SUCCESS(f"Grupo creado: {nombre_grupo}"))
            else:
                self.stdout.write(f"Grupo actualizado: {nombre_grupo}")

            self.stdout.write(
                f"  {configuracion['descripcion']} Permisos asignados: {len(permisos)}"
            )

        for username in options["admin_user"]:
            try:
                usuario = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f"No existe el usuario: {username}")

            usuario.groups.add(grupos["Administradores"])
            self.stdout.write(
                self.style.SUCCESS(
                    f"Usuario {username} añadido al grupo Administradores."
                )
            )

        self.stdout.write(self.style.SUCCESS("Inicialización de grupos completada."))

    def obtener_permisos(self, permisos_configurados):
        if permisos_configurados == "__all__":
            return Permission.objects.all()

        permisos = []
        for app_label, codename in permisos_configurados:
            permiso = Permission.objects.filter(
                content_type__app_label=app_label,
                codename=codename,
            ).first()

            if permiso:
                permisos.append(permiso)
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Permiso no encontrado: {app_label}.{codename}"
                    )
                )

        return permisos
