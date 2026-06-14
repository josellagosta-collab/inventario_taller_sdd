from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea los grupos base de la aplicación y permite asignar usuarios."

    def add_arguments(self, parser):
        parser.add_argument(
            "--admin-user",
            action="append",
            default=[],
            help="Username que se añadirá al grupo Administradores. Se puede usar varias veces.",
        )

    def handle(self, *args, **options):
        grupo, creado = Group.objects.get_or_create(name="Administradores")

        if creado:
            self.stdout.write(self.style.SUCCESS("Grupo creado: Administradores"))
        else:
            self.stdout.write("El grupo Administradores ya existe.")

        for username in options["admin_user"]:
            try:
                usuario = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f"No existe el usuario: {username}")

            usuario.groups.add(grupo)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Usuario {username} añadido al grupo Administradores."
                )
            )

        self.stdout.write(self.style.SUCCESS("Inicialización de grupos completada."))
