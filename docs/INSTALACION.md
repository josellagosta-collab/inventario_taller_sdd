# Instalación - Inventario Taller SDD

Guía para instalar el proyecto en un entorno local de desarrollo.

## Requisitos previos

- Windows con PowerShell.
- Python 3.13 o compatible con Django 6.
- PostgreSQL instalado y en ejecución.
- Git.
- Acceso al código del proyecto.

## 1. Obtener el proyecto

Clonar el repositorio o situarse en la carpeta del proyecto:

```powershell
cd F:\proyectos_SDD\inventrario_taller_ssd
```

## 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

Activar el entorno:

```powershell
.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación por política de ejecución, abrir PowerShell como usuario actual y ejecutar:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Después volver a activar el entorno virtual.

## 3. Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dependencias principales:

- Django.
- PostgreSQL driver `psycopg2-binary`.
- Pillow para imágenes.

## 4. Preparar PostgreSQL

La configuración actual del proyecto espera estos datos:

```txt
Base de datos: inventario_taller
Usuario: inventario_user
Host: localhost
Puerto: 5432
```

Crear la base de datos y el usuario desde PostgreSQL según la instalación local.

Ejemplo orientativo desde `psql` con un usuario administrador:

```sql
CREATE DATABASE inventario_taller;
CREATE USER inventario_user WITH PASSWORD 'Inventario1234';
GRANT ALL PRIVILEGES ON DATABASE inventario_taller TO inventario_user;
```

En PostgreSQL recientes puede ser necesario conceder permisos sobre el esquema público:

```sql
\c inventario_taller
GRANT ALL ON SCHEMA public TO inventario_user;
```

## 5. Aplicar migraciones

Con el entorno virtual activo:

```powershell
python manage.py migrate
```

## 6. Crear usuario administrador

Crear un superusuario de Django:

```powershell
python manage.py createsuperuser
```

Después inicializar los grupos base y asignar el usuario creado al grupo `Administradores`:

```powershell
python manage.py inicializar_grupos --admin-user nombre_usuario
```

El comando crea o actualiza estos grupos:

- `Administradores`
- `Profesores`
- `Técnicos`
- `Alumnos`

## 7. Cargar datos iniciales opcionales

Si se quieren cargar categorías o materiales de ejemplo, revisar y ejecutar los scripts disponibles en la raíz:

```powershell
python cargar_categorias.py
python cargar_materiales.py
```

Ejecutarlos solo después de tener la base de datos migrada.

## 8. Arrancar el servidor

```powershell
python manage.py runserver
```

Abrir en el navegador:

```txt
http://127.0.0.1:8000/
```

## 9. Comprobar instalación

Ejecutar comprobación de Django:

```powershell
python manage.py check
```

Ejecutar pruebas:

```powershell
python manage.py test --keepdb --noinput
```

Si es la primera ejecución y no existe base de datos de pruebas, Django intentará crear `test_inventario_taller`.

## 10. Rutas útiles

- Dashboard: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login/`
- Administración Django: `http://127.0.0.1:8000/admin/`
- Materiales: `http://127.0.0.1:8000/materiales/`
- Préstamos: `http://127.0.0.1:8000/prestamos/`
- Auditoría: `http://127.0.0.1:8000/auditoria/`

## Problemas frecuentes

### Django no está instalado

Verificar que el entorno virtual está activo:

```powershell
.venv\Scripts\Activate.ps1
python -m django --version
```

### Error de conexión con PostgreSQL

Comprobar:

- PostgreSQL está arrancado.
- Existe la base de datos `inventario_taller`.
- Existe el usuario `inventario_user`.
- La contraseña coincide con la configuración del proyecto.
- El puerto local es `5432`.

### No se puede crear la base de datos de pruebas

El usuario PostgreSQL necesita permisos para crear bases de datos de test o debe existir una base `test_inventario_taller` accesible.

Como alternativa temporal en desarrollo, ejecutar pruebas con:

```powershell
python manage.py test --keepdb --noinput
```

## Siguiente documentación relacionada

- `README.md`
- `docs/BACKLOG.md`
- `docs/JIRA_SYNC.md`
