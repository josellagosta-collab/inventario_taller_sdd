# Despliegue - Inventario Taller SDD

Guía para preparar el proyecto para un entorno de producción o preproducción.

> Estado actual: el proyecto está configurado para desarrollo local. Antes de publicar la aplicación hay que revisar seguridad, variables de entorno, archivos estáticos, media, base de datos y servidor de aplicación.

## 1. Objetivo del despliegue

Publicar la aplicación Django para que los usuarios puedan acceder desde navegador a:

- Dashboard.
- Inventario.
- Ubicaciones.
- Préstamos y reservas.
- Incidencias.
- Mantenimiento.
- Documentos y fotografías.
- Auditoría.
- Informes.

## 2. Requisitos del servidor

- Python 3.13 o compatible con Django 6.
- PostgreSQL.
- Servidor web o proxy inverso.
- Servicio WSGI/ASGI para ejecutar Django.
- Espacio persistente para `media/`.
- Carpeta persistente para `logs/`.
- Copias de seguridad configuradas.

## 3. Configuración que no debe usarse tal cual en producción

El archivo actual `inventario_taller/settings.py` contiene valores válidos para desarrollo:

```python
DEBUG = True
ALLOWED_HOSTS = []
SECRET_KEY = "..."
```

Antes de desplegar:

- `DEBUG` debe ser `False`.
- `SECRET_KEY` debe salir de una variable de entorno.
- `ALLOWED_HOSTS` debe contener el dominio o IP de producción.
- La contraseña de PostgreSQL no debe estar escrita en código.
- `EMAIL_BACKEND` debe cambiarse si se van a enviar correos reales.

Ejemplo de variables de entorno recomendadas:

```txt
DJANGO_SECRET_KEY=clave-segura
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=inventario.midominio.local,127.0.0.1
POSTGRES_DB=inventario_taller
POSTGRES_USER=inventario_user
POSTGRES_PASSWORD=contraseña-segura
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## 4. Preparar el código en el servidor

Clonar o copiar el proyecto:

```powershell
git clone URL_DEL_REPOSITORIO inventario_taller_ssd
cd inventario_taller_ssd
```

Crear entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Base de datos

Crear la base de datos PostgreSQL y el usuario de aplicación.

Ejemplo desde `psql`:

```sql
CREATE DATABASE inventario_taller;
CREATE USER inventario_user WITH PASSWORD 'contraseña-segura';
GRANT ALL PRIVILEGES ON DATABASE inventario_taller TO inventario_user;
\c inventario_taller
GRANT ALL ON SCHEMA public TO inventario_user;
```

La documentación específica de base de datos se completará en `BL-121`.

## 6. Migraciones y datos base

Aplicar migraciones:

```powershell
python manage.py migrate
```

Crear superusuario:

```powershell
python manage.py createsuperuser
```

Inicializar grupos y permisos:

```powershell
python manage.py inicializar_grupos --admin-user nombre_usuario
```

## 7. Archivos estáticos

En producción Django no debe servir estáticos con `DEBUG=True`.

Antes del despliegue hay que configurar `STATIC_ROOT` en settings de producción, por ejemplo:

```python
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Después ejecutar:

```powershell
python manage.py collectstatic
```

El servidor web debe publicar el contenido de `STATIC_ROOT`.

## 8. Archivos media

Los documentos y fotografías se guardan en:

```txt
MEDIA_ROOT = BASE_DIR / "media"
```

En producción:

- `media/` debe estar en almacenamiento persistente.
- Debe incluirse en la política de copias de seguridad.
- El servidor web debe servir `MEDIA_URL`.
- Deben revisarse permisos de lectura/escritura para el usuario que ejecuta Django.

## 9. Logs

La aplicación escribe logs en:

```txt
logs/django.log
logs/security.log
```

En producción:

- Crear la carpeta `logs/`.
- Dar permisos de escritura al usuario de la aplicación.
- Configurar rotación de logs.
- Revisar periódicamente `security.log`.

## 10. Servidor de aplicación

Django debe ejecutarse detrás de un servidor WSGI/ASGI.

Opciones habituales:

- Gunicorn o uWSGI en Linux.
- Waitress en Windows.
- Daphne/Uvicorn si se decide usar ASGI.

Ejemplo orientativo con Waitress en Windows:

```powershell
pip install waitress
waitress-serve --listen=127.0.0.1:8000 inventario_taller.wsgi:application
```

Si se adopta Waitress, Gunicorn u otro servidor, debe añadirse a `requirements.txt`.

## 11. Proxy inverso

Se recomienda colocar un proxy inverso delante de Django:

- Nginx.
- Apache.
- IIS.

Responsabilidades del proxy:

- Terminar HTTPS.
- Servir estáticos.
- Servir media.
- Redirigir HTTP a HTTPS.
- Reenviar tráfico dinámico al servidor WSGI/ASGI.

## 12. Comprobaciones antes de publicar

Ejecutar:

```powershell
python manage.py check --deploy
python manage.py migrate --check
python manage.py test --keepdb --noinput
```

Verificar manualmente:

- Login.
- Logout.
- Acceso al admin.
- Dashboard.
- Listado de materiales.
- Subida y descarga de documentos.
- Subida de fotografías.
- Creación y devolución de préstamos.
- Auditoría.
- Informes.

## 13. Checklist de seguridad

- `DEBUG=False`.
- `SECRET_KEY` fuera del repositorio.
- Credenciales de base de datos fuera del repositorio.
- `ALLOWED_HOSTS` configurado.
- HTTPS activo.
- Copias de seguridad de PostgreSQL.
- Copias de seguridad de `media/`.
- Logs persistentes y rotados.
- Usuario administrador revisado.
- Grupos inicializados con `inicializar_grupos`.
- Permisos del sistema de archivos limitados.

## 14. Proceso recomendado de actualización

1. Hacer copia de seguridad de PostgreSQL.
2. Hacer copia de seguridad de `media/`.
3. Descargar nueva versión del código.
4. Instalar nuevas dependencias.
5. Ejecutar migraciones.
6. Ejecutar `collectstatic`.
7. Reiniciar servicio WSGI/ASGI.
8. Revisar logs.
9. Probar flujos principales.

## 15. Estado pendiente

Esta guía documenta el procedimiento objetivo. Para un despliegue real todavía conviene preparar:

- Settings separados para producción.
- Lectura de configuración desde variables de entorno.
- Servidor WSGI/ASGI elegido y añadido a dependencias.
- Configuración exacta del proxy inverso.
- Estrategia de backups.
- Automatización de despliegue.
