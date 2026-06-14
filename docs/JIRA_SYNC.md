# Sincronización manual con Jira

Este proyecto incluye un comando de Django para sincronizar `docs/BACKLOG.md` con Jira Cloud de forma manual e incremental.

## Variables de entorno

En PowerShell, configura tus datos antes de ejecutar el comando:

```powershell
$env:JIRA_BASE_URL="https://tu-dominio.atlassian.net"
$env:JIRA_EMAIL="tu-email"
$env:JIRA_API_TOKEN="tu-token"
$env:JIRA_PROJECT_KEY="CLAVE"
```

Opcionalmente puedes ajustar nombres de tipos y estados si tu Jira los tiene traducidos:

```powershell
$env:JIRA_EPIC_ISSUE_TYPE="Epic"
$env:JIRA_STORY_ISSUE_TYPE="Story"
$env:JIRA_TASK_ISSUE_TYPE="Task"
$env:JIRA_STATUS_TODO="To Do"
$env:JIRA_STATUS_IN_PROGRESS="In Progress"
$env:JIRA_STATUS_DONE="Done"
$env:JIRA_STATUS_REVIEW="In Review"
```

## Archivos locales

El comando usa dos archivos:

```text
docs/jira_sync_map.json
docs/jira_sync_state.json
```

`jira_sync_map.json` relaciona cada `BL-*` con su issue de Jira.

`jira_sync_state.json` guarda la última versión sincronizada de cada elemento. Gracias a este archivo, las siguientes sincronizaciones solo envían a Jira lo que ha cambiado.

## Inicializar sincronización incremental

Si ya tienes Jira sincronizado y quieres evitar que el comando vuelva a actualizar las 122 tareas una por una, ejecuta una vez:

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira --tasks-only --init-state
```

Esto no llama a Jira. Solo crea o actualiza `docs/jira_sync_state.json` tomando el backlog actual como punto de partida.

## Previsualizar cambios

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira --tasks-only
```

No llama a Jira. Muestra únicamente las tareas nuevas o modificadas.

Para ver también las tareas sin cambios:

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira --tasks-only --show-all
```

## Sincronizar solo cambios

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira --tasks-only --apply
```

El comando solo crea o actualiza los elementos que hayan cambiado respecto a `docs/jira_sync_state.json`.

## Forzar sincronización completa

Si necesitas reenviar todo a Jira:

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira --tasks-only --apply --force
```

## Notas

- No guardes nunca el token dentro del código.
- Si tu flujo de Jira no usa `To Do`, `In Progress` o `Done`, configura las variables `JIRA_STATUS_*`.
- En Jira gratuito puede variar la disponibilidad de tipos como `Epic` o `Story` según el tipo de proyecto.
