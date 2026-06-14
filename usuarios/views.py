import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from auditoria.services import registrar_accion

from .decorators import pertenece_a_grupo
from .forms import RolForm, UsuarioCrearForm, UsuarioEditarForm, UsuarioPasswordForm


security_logger = logging.getLogger("seguridad")
ROLES_PROTEGIDOS = ["Administradores"]


@login_required
@pertenece_a_grupo("Administradores")
def lista_usuarios(request):
    usuarios = User.objects.prefetch_related("groups").order_by("username")

    busqueda = request.GET.get("busqueda", "")
    estado = request.GET.get("estado", "")

    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda) |
            Q(email__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda)
        )

    if estado == "activos":
        usuarios = usuarios.filter(is_active=True)
    elif estado == "inactivos":
        usuarios = usuarios.filter(is_active=False)

    paginator = Paginator(usuarios, 10)
    pagina_usuarios = paginator.get_page(request.GET.get("page"))

    for usuario in pagina_usuarios:
        usuario.es_administrador = (
            usuario.is_superuser or
            usuario.groups.filter(name="Administradores").exists()
        )

    return render(request, "usuarios/lista_usuarios.html", {
        "usuarios": pagina_usuarios,
        "busqueda": busqueda,
        "estado": estado,
    })


@login_required
@pertenece_a_grupo("Administradores")
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioCrearForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            registrar_accion(
                request,
                "crear",
                f"Usuario creado: {usuario.username}",
                usuario
            )
            security_logger.info(
                "Usuario creado usuario=%s creado_por=%s",
                usuario.username,
                request.user.username,
            )
            messages.success(request, "Usuario creado correctamente.")
            return redirect("usuarios:lista_usuarios")
    else:
        form = UsuarioCrearForm(initial={"is_active": True})

    return render(request, "usuarios/form_usuario.html", {
        "form": form,
        "titulo": "Nuevo usuario",
        "texto_boton": "Crear usuario",
    })


@login_required
@pertenece_a_grupo("Administradores")
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    if request.method == "POST":
        form = UsuarioEditarForm(request.POST, instance=usuario)

        if form.is_valid():
            usuario = form.save()
            registrar_accion(
                request,
                "editar",
                f"Usuario editado: {usuario.username}",
                usuario
            )
            security_logger.info(
                "Usuario editado usuario=%s editado_por=%s",
                usuario.username,
                request.user.username,
            )
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("usuarios:lista_usuarios")
    else:
        form = UsuarioEditarForm(instance=usuario)

    return render(request, "usuarios/form_usuario.html", {
        "form": form,
        "titulo": f"Editar usuario: {usuario.username}",
        "texto_boton": "Guardar cambios",
        "usuario_editado": usuario,
    })


@login_required
@pertenece_a_grupo("Administradores")
def cambiar_password_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    if request.method == "POST":
        form = UsuarioPasswordForm(usuario, request.POST)

        if form.is_valid():
            form.save()
            registrar_accion(
                request,
                "editar",
                f"Contraseña cambiada para el usuario: {usuario.username}",
                usuario
            )
            security_logger.info(
                "Contraseña cambiada usuario=%s cambiada_por=%s",
                usuario.username,
                request.user.username,
            )
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect("usuarios:lista_usuarios")
    else:
        form = UsuarioPasswordForm(usuario)

    return render(request, "usuarios/form_usuario.html", {
        "form": form,
        "titulo": f"Cambiar contraseña: {usuario.username}",
        "texto_boton": "Cambiar contraseña",
        "usuario_editado": usuario,
    })


@login_required
@pertenece_a_grupo("Administradores")
def desactivar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    if request.method == "POST":
        if usuario == request.user:
            messages.error(request, "No puedes desactivar tu propio usuario.")
            return redirect("usuarios:lista_usuarios")

        usuario.is_active = False
        usuario.save(update_fields=["is_active"])
        registrar_accion(
            request,
            "editar",
            f"Usuario desactivado: {usuario.username}",
            usuario
        )
        security_logger.warning(
            "Usuario desactivado usuario=%s desactivado_por=%s",
            usuario.username,
            request.user.username,
        )
        messages.success(request, "Usuario desactivado correctamente.")
        return redirect("usuarios:lista_usuarios")

    return render(request, "usuarios/desactivar_usuario.html", {
        "usuario_editado": usuario,
    })


@login_required
@pertenece_a_grupo("Administradores")
def lista_roles(request):
    roles = Group.objects.prefetch_related("permissions", "user_set").order_by("name")
    busqueda = request.GET.get("busqueda", "")

    if busqueda:
        roles = roles.filter(name__icontains=busqueda)

    paginator = Paginator(roles, 10)
    pagina_roles = paginator.get_page(request.GET.get("page"))

    for rol in pagina_roles:
        rol.es_protegido = rol.name in ROLES_PROTEGIDOS
        rol.total_usuarios = rol.user_set.count()
        rol.total_permisos = rol.permissions.count()

    return render(request, "usuarios/lista_roles.html", {
        "roles": pagina_roles,
        "busqueda": busqueda,
    })


@login_required
@pertenece_a_grupo("Administradores")
def crear_rol(request):
    if request.method == "POST":
        form = RolForm(request.POST)

        if form.is_valid():
            rol = form.save()
            registrar_accion(
                request,
                "crear",
                f"Rol creado: {rol.name}",
                rol
            )
            security_logger.info(
                "Rol creado rol=%s creado_por=%s",
                rol.name,
                request.user.username,
            )
            messages.success(request, "Rol creado correctamente.")
            return redirect("usuarios:lista_roles")
    else:
        form = RolForm()

    return render(request, "usuarios/form_rol.html", {
        "form": form,
        "titulo": "Nuevo rol",
        "texto_boton": "Crear rol",
    })


@login_required
@pertenece_a_grupo("Administradores")
def editar_rol(request, rol_id):
    rol = get_object_or_404(Group, id=rol_id)

    if request.method == "POST":
        form = RolForm(request.POST, instance=rol)

        if form.is_valid():
            rol = form.save()
            registrar_accion(
                request,
                "editar",
                f"Rol editado: {rol.name}",
                rol
            )
            security_logger.info(
                "Rol editado rol=%s editado_por=%s",
                rol.name,
                request.user.username,
            )
            messages.success(request, "Rol actualizado correctamente.")
            return redirect("usuarios:lista_roles")
    else:
        form = RolForm(instance=rol)

    return render(request, "usuarios/form_rol.html", {
        "form": form,
        "titulo": f"Editar rol: {rol.name}",
        "texto_boton": "Guardar cambios",
        "rol": rol,
    })


@login_required
@pertenece_a_grupo("Administradores")
def eliminar_rol(request, rol_id):
    rol = get_object_or_404(Group, id=rol_id)

    if rol.name in ROLES_PROTEGIDOS:
        messages.error(request, "Este rol está protegido y no se puede eliminar.")
        return redirect("usuarios:lista_roles")

    usuarios_asignados = rol.user_set.count()

    if request.method == "POST":
        if usuarios_asignados:
            messages.error(
                request,
                "No se puede eliminar un rol con usuarios asignados."
            )
            return redirect("usuarios:lista_roles")

        nombre_rol = rol.name
        registrar_accion(
            request,
            "eliminar",
            f"Rol eliminado: {nombre_rol}",
            rol
        )
        rol.delete()
        security_logger.warning(
            "Rol eliminado rol=%s eliminado_por=%s",
            nombre_rol,
            request.user.username,
        )
        messages.success(request, "Rol eliminado correctamente.")
        return redirect("usuarios:lista_roles")

    return render(request, "usuarios/eliminar_rol.html", {
        "rol": rol,
        "usuarios_asignados": usuarios_asignados,
    })
