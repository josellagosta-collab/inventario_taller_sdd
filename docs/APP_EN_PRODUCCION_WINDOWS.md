# APP_EN_PRODUCCION_WINDOWS.md

# Despliegue de Inventario de Taller v1.0 en Windows 11 con Docker

## 1. Objetivo

Este documento explica cómo poner en producción la aplicación **Inventario de Taller v1.0** en una máquina con **Windows 11**, usando dos contenedores Docker:

- Contenedor 1: aplicación Django.
- Contenedor 2: base de datos PostgreSQL.

La aplicación será accesible desde cualquier equipo de la red local mediante:

```text
http://172.16.4.124:8000
```

Además, los contenedores quedarán configurados para arrancar automáticamente cuando se inicie Windows y Docker Desktop.

---

## 2. Arquitectura final

```text
Windows 11
│
├── Docker Desktop
│
├── Contenedor inventario_taller_web
│   ├── Django
│   ├── Gunicorn
│   ├── WhiteNoise
│   └── Archivos estáticos
│
└── Contenedor inventario_taller_db
    └── PostgreSQL
```

---

## 3. Requisitos previos

Instalar **Docker Desktop** en Windows 11.

Durante la instalación, activar:

```text
Use WSL 2 based engine
```

Después, abrir Docker Desktop y comprobar:

```text
Settings → General
```

Activar:

```text
Start Docker Desktop when you sign in to your computer
Use the WSL 2 based engine
```

---

## 4. Estructura esperada del proyecto

En la carpeta raíz del proyecto, donde está `manage.py`, deben existir estos archivos:

```text
inventario_taller_sdd/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env
├── requirements.txt
├── manage.py
│
├── inventario_taller/
├── static/
├── staticfiles/
└── media/
```

---

## 5. Archivo `requirements.txt`

Desde PowerShell, dentro del entorno virtual del proyecto:

```powershell
pip freeze > requirements.txt
```

Debe incluir, como mínimo:

```text
Django
gunicorn
psycopg2-binary
whitenoise
Pillow
openpyxl
reportlab
python-dotenv
```

Si falta `whitenoise`:

```powershell
pip install whitenoise
pip freeze > requirements.txt
```

Si falta `gunicorn`:

```powershell
pip install gunicorn
pip freeze > requirements.txt
```

---

## 6. Archivo `.env`

Crear en la raíz del proyecto:

```env
DEBUG=False

SECRET_KEY=CAMBIA_ESTA_CLAVE_POR_UNA_CLAVE_SEGURA

POSTGRES_DB=inventario_taller
POSTGRES_USER=inventario_user
POSTGRES_PASSWORD=Inventario1234
POSTGRES_HOST=db
POSTGRES_PORT=5432

ALLOWED_HOSTS=localhost,127.0.0.1,172.16.4.124
CSRF_TRUSTED_ORIGINS=http://172.16.4.124:8000
```

> Importante: en producción, cambia `SECRET_KEY` y `POSTGRES_PASSWORD` por valores seguros.

---

## 7. Archivo `.dockerignore`

Crear en la raíz del proyecto:

```text
.venv
.venv-1
__pycache__
*.pyc
.git
.gitignore
db.sqlite3
```

No se han excluido `media` ni `static`, porque queremos que Docker pueda copiar los archivos iniciales del proyecto. La persistencia de `media` y `staticfiles` se gestiona mediante volúmenes.

---

## 8. Archivo `Dockerfile`

Crear en la raíz del proyecto:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "inventario_taller.wsgi:application", "--bind", "0.0.0.0:8000"]
```

> No se usa `entrypoint.sh`, porque en Windows dio problemas con saltos de línea. La solución final funcional usa `command` directamente en `docker-compose.yml`.

---

## 9. Archivo `docker-compose.yml`

Crear en la raíz del proyecto:

```yaml
services:

  db:
    image: postgres:15
    container_name: inventario_taller_db
    restart: unless-stopped

    environment:
      POSTGRES_DB: inventario_taller
      POSTGRES_USER: inventario_user
      POSTGRES_PASSWORD: Inventario1234

    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    container_name: inventario_taller_web
    restart: unless-stopped

    env_file:
      - .env

    ports:
      - "8000:8000"

    depends_on:
      - db

    volumes:
      - media_data:/app/media
      - static_data:/app/staticfiles

    command: >
      sh -c "python manage.py migrate --noinput &&
             python manage.py collectstatic --noinput &&
             gunicorn inventario_taller.wsgi:application --bind 0.0.0.0:8000"

volumes:
  postgres_data:
  media_data:
  static_data:
```

---

## 10. Configuración necesaria en `settings.py`

Archivo:

```text
inventario_taller/settings.py
```

### 10.1 Importar `os`

Al principio del archivo:

```python
import os
from pathlib import Path
```

---

### 10.2 `DEBUG`

```python
DEBUG = os.getenv("DEBUG", "False") == "True"
```

---

### 10.3 `ALLOWED_HOSTS`

```python
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")
```

---

### 10.4 Base de datos PostgreSQL

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "inventario_taller"),
        "USER": os.getenv("POSTGRES_USER", "inventario_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "Inventario1234"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
```

---

### 10.5 Middleware con WhiteNoise

En `MIDDLEWARE`, debe estar WhiteNoise justo después de `SecurityMiddleware`:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

---

### 10.6 Archivos estáticos

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

---

### 10.7 Archivos media

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

---

### 10.8 Configuración de WhiteNoise en `STORAGES`

```python
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
```

---

### 10.9 Orígenes CSRF

```python
CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    ""
).split(",") if os.getenv("CSRF_TRUSTED_ORIGINS") else []
```

---

## 11. Configuración de `urls.py`

Archivo:

```text
inventario_taller/urls.py
```

Debe tener estos imports:

```python
from django.conf import settings
from django.conf.urls.static import static
```

Y al final del archivo:

```python
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
```

Ejemplo completo simplificado:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("", include("inventario.urls")),
    path("", include("documentos.urls")),
    path("", include("prestamos.urls")),
    path("", include("incidencias.urls")),
    path("", include("informes.urls")),
    path("", include("auditoria.urls")),
    path("", include("ubicaciones.urls")),
    path("", include("usuarios.urls")),
    path("", include("mantenimiento.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
```

---

## 12. Comprobar el logo y archivos estáticos

El logo debe estar en:

```text
static/images/logo_monlau.png
```

En la plantilla base:

```html
{% load static %}

<img src="{% static 'images/logo_monlau.png' %}"
     alt="Logo Monlau"
     height="60">
```

Después de arrancar Docker, se podrá comprobar con:

```text
http://127.0.0.1:8000/static/images/logo_monlau.png
```

---

## 13. Construcción de los contenedores

Abrir PowerShell en la raíz del proyecto:

```powershell
cd C:\Users\aguileraj\Documents\Proyectos\inventario_taller_sdd
```

Construir sin caché:

```powershell
docker compose build --no-cache
```

Arrancar:

```powershell
docker compose up -d
```

---

## 14. Verificar estado de los contenedores

```powershell
docker compose ps
```

Debe aparecer algo parecido a:

```text
inventario_taller_db    Up
inventario_taller_web   Up
```

---

## 15. Ver logs

```powershell
docker compose logs web --tail=100
```

Si todo va bien, deben aparecer mensajes similares a:

```text
Applying migrations...
collectstatic...
Starting gunicorn...
Listening at: http://0.0.0.0:8000
```

---

## 16. Crear superusuario

Cuando el contenedor `web` esté en estado `Up`:

```powershell
docker compose exec web python manage.py createsuperuser
```

---

## 17. Acceso local

Desde la propia máquina Windows 11:

```text
http://127.0.0.1:8000
```

---

## 18. Acceso desde la red

Desde cualquier equipo de la red local:

```text
http://172.16.4.124:8000
```

---

## 19. Firewall de Windows

Si desde otros equipos no se puede acceder, crear una regla de entrada en el Firewall de Windows:

```text
Tipo: Puerto
Protocolo: TCP
Puerto: 8000
Acción: Permitir conexión
Perfil: Privado
Nombre: Inventario Taller Django 8000
```

---

## 20. Arranque automático al iniciar Windows

Docker Desktop debe tener activado:

```text
Start Docker Desktop when you sign in to your computer
```

Y los contenedores tienen:

```yaml
restart: unless-stopped
```

Por tanto, al iniciar Windows y arrancar Docker Desktop, los contenedores volverán a levantarse automáticamente.

---

## 21. Comandos útiles

### Parar contenedores

```powershell
docker compose down
```

### Arrancar contenedores

```powershell
docker compose up -d
```

### Reconstruir contenedores

```powershell
docker compose build --no-cache
docker compose up -d
```

### Ver logs del contenedor web

```powershell
docker compose logs web --tail=100
```

### Entrar al contenedor web

```powershell
docker compose exec web bash
```

### Ejecutar migraciones manualmente

```powershell
docker compose exec web python manage.py migrate
```

### Ejecutar collectstatic manualmente

```powershell
docker compose exec web python manage.py collectstatic --noinput
```

---

## 22. Copias de seguridad de PostgreSQL

### Crear backup

```powershell
docker compose exec db pg_dump -U inventario_user inventario_taller > backup_inventario.sql
```

### Restaurar backup

```powershell
docker compose exec -T db psql -U inventario_user inventario_taller < backup_inventario.sql
```

---

## 23. Comprobaciones finales

Abrir:

```text
http://127.0.0.1:8000
```

Comprobar:

- Login.
- Dashboard.
- Listado de materiales.
- Alta de material.
- Reservas.
- Préstamos.
- Incidencias.
- Informes PDF y Excel.
- Logo corporativo.
- Fotografías y documentos.

Después probar desde otro PC:

```text
http://172.16.4.124:8000
```

---

## 24. Resultado final

La aplicación Inventario de Taller v1.0 queda desplegada en Windows 11 mediante Docker con:

- Django + Gunicorn.
- PostgreSQL.
- WhiteNoise para archivos estáticos.
- Volúmenes persistentes.
- Acceso desde red local.
- Arranque automático con Docker Desktop.

URL final:

```text
http://172.16.4.124:8000
```
