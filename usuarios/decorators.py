from django.contrib.auth.decorators import user_passes_test


def pertenece_a_grupo(nombre_grupo):
    def comprobar(user):
        return user.is_authenticated and user.groups.filter(name=nombre_grupo).exists()

    return user_passes_test(comprobar)