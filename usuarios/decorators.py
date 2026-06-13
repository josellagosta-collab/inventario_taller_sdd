from django.contrib.auth.decorators import user_passes_test


def pertenece_a_grupo(nombre_grupo):

    def comprobar(user):

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.groups.filter(
            name=nombre_grupo
        ).exists()

    return user_passes_test(comprobar)