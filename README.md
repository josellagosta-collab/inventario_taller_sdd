# Inventario Taller SDD

Aplicación web Django para gestionar de forma centralizada el inventario de un taller de hardware.

El sistema permite registrar materiales, ubicarlos físicamente, controlar préstamos y reservas, documentar incidencias, registrar mantenimientos, adjuntar documentación y consultar auditoría e informes.

## Estado del proyecto

- Versión objetivo: 1.0
- Metodología: SDD
- Backend: Python + Django
- Base de datos: PostgreSQL
- Idioma y zona horaria: `es-es`, `Europe/Madrid`

El MVP funcional incluye usuarios, inventario, ubicaciones, préstamos, movimientos y auditoría. El bloque de pruebas del backlog está completado.

## Módulos principales

- `usuarios`: login, logout, recuperación de contraseña, perfiles, grupos y roles.
- `inventario`: materiales, categorías, proveedores, estados, dashboard y movimientos.
- `ubicaciones`: edificios, aulas, armarios, estanterías, cajas y ubicaciones completas.
- `prestamos`: préstamos, devoluciones, reservas, cancelaciones y conversión de reservas.
- `incidencias`: alta, listado, detalle y resolución de incidencias.
- `mantenimiento`: mantenimientos, planes y alertas de revisión.
- `documentos`: documentos y fotografías asociados a materiales.
- `auditoria`: registro de acciones importantes del sistema.
- `informes`: informes de inventario, préstamos, incidencias y económico.

## Requisitos

- Python 3.13 o compatible con Django 6.
- PostgreSQL.
- Entorno virtual Python.

Dependencias principales:

```txt
Django==6.0.6
Pillow==12.2.0
psycopg2-binary==2.9.12
```

## Configuración rápida en desarrollo

Crear y activar el entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Aplicar migraciones:

```powershell
python manage.py migrate
```

Crear o actualizar grupos base:

```powershell
python manage.py inicializar_grupos
```

Asignar un usuario al grupo `Administradores`:

```powershell
python manage.py inicializar_grupos --admin-user nombre_usuario
```

Arrancar el servidor de desarrollo:

```powershell
python manage.py runserver
```

## Base de datos

La configuración actual usa PostgreSQL local:

```txt
DB: inventario_taller
USER: inventario_user
HOST: localhost
PORT: 5432
```

La documentación detallada de instalación, despliegue y base de datos se mantiene como tareas específicas del backlog.

## Pruebas

Ejecutar toda la suite:

```powershell
python manage.py test
```

Ejecutar suites concretas:

```powershell
python manage.py test inventario prestamos usuarios
```

Cuando se trabaje con PostgreSQL y una base de pruebas ya existente:

```powershell
python manage.py test --keepdb --noinput
```

El proyecto incluye pruebas de:

- Modelos.
- Formularios.
- Vistas.
- Permisos.
- Integración entre módulos.
- Rendimiento basado en número de consultas.

## Documentación del proyecto

- `docs/INSTALACION.md`: instalación local del proyecto.
- `docs/DESPLIEGUE.md`: preparación para producción o preproducción.
- `docs/PRD.md`: requisitos del producto.
- `docs/SSD.md`: diseño del sistema.
- `docs/MODELO_DATOS.md`: modelo de datos.
- `docs/BACKLOG.md`: épicas, historias de usuario y tareas técnicas.
- `docs/JIRA_SYNC.md`: sincronización del backlog con Jira.

## Sincronización con Jira

Para sincronizar tareas del backlog con Jira:

```powershell
python.exe manage.py sync_backlog_jira --tasks-only --apply
```

Revisar antes `docs/JIRA_SYNC.md` para confirmar el flujo esperado.
