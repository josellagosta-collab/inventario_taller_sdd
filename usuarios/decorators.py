from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps


def pertenece_a_grupo(nombre_grupo):

    def comprobar(user):

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        return user.groups.filter(
            name=nombre_grupo
        ).exists()

    def decorador(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if comprobar(request.user):
                return view_func(request, *args, **kwargs)

            if request.user.is_authenticated:
                raise PermissionDenied

            return user_passes_test(comprobar)(view_func)(request, *args, **kwargs)

        return wrapper

    return decorador
