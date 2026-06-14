# Sincronización manual con Jira

Este proyecto incluye un comando de Django para sincronizar `docs/BACKLOG.md` con Jira Cloud de forma manual.

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

## Previsualizar

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira
```

No llama a Jira. Solo muestra qué elementos detecta.

## Sincronizar

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira --apply
```

El comando crea o actualiza issues y guarda el vínculo local en:

```text
docs/jira_sync_map.json
```

Ese archivo evita duplicar issues en futuras sincronizaciones.

## Sincronizar solo tareas BL

```powershell
.\.venv\Scripts\python.exe manage.py sync_backlog_jira --tasks-only --apply
```

## Notas

- No guardes nunca el token dentro del código.
- Si tu flujo de Jira no usa `To Do`, `In Progress` o `Done`, configura las variables `JIRA_STATUS_*`.
- En Jira gratuito puede variar la disponibilidad de tipos como `Epic` o `Story` según el tipo de proyecto.
