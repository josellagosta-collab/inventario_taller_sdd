import base64
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


BACKLOG_EPIC_RE = re.compile(r"^# (EP\d+) - (.+)$")
BACKLOG_STORY_RE = re.compile(r"^## (HU\d+) - (.+)$")
BACKLOG_TASK_RE = re.compile(r"^- (BL-\d+) \[(.+?)\] (.+?)\.?$")


class JiraClient:
    def __init__(self, base_url, email, api_token):
        self.base_url = base_url.rstrip("/")
        token = f"{email}:{api_token}".encode("utf-8")
        self.auth_header = base64.b64encode(token).decode("ascii")

    def request(self, method, path, data=None):
        body = None
        headers = {
            "Authorization": f"Basic {self.auth_header}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if data is not None:
            body = json.dumps(data).encode("utf-8")

        request = Request(
            f"{self.base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )

        try:
            with urlopen(request, timeout=30) as response:
                content = response.read().decode("utf-8")
                return json.loads(content) if content else {}
        except HTTPError as error:
            detail = error.read().decode("utf-8")
            raise CommandError(
                f"Jira API error {error.code} calling {method} {path}: {detail}"
            )

    def create_issue(self, fields):
        return self.request("POST", "/rest/api/3/issue", {"fields": fields})

    def update_issue(self, issue_key, fields):
        self.request("PUT", f"/rest/api/3/issue/{issue_key}", {"fields": fields})

    def get_transitions(self, issue_key):
        response = self.request("GET", f"/rest/api/3/issue/{issue_key}/transitions")
        return response.get("transitions", [])

    def transition_issue(self, issue_key, transition_id):
        self.request(
            "POST",
            f"/rest/api/3/issue/{issue_key}/transitions",
            {"transition": {"id": transition_id}},
        )


class Command(BaseCommand):
    help = "Sincroniza docs/BACKLOG.md con Jira de forma manual."

    def add_arguments(self, parser):
        parser.add_argument(
            "--backlog",
            default=str(settings.BASE_DIR / "docs" / "BACKLOG.md"),
            help="Ruta del backlog Markdown.",
        )
        parser.add_argument(
            "--map",
            default=str(settings.BASE_DIR / "docs" / "jira_sync_map.json"),
            help="Ruta del archivo local que relaciona IDs del backlog con issues Jira.",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Crea o actualiza issues en Jira. Sin este flag solo muestra un resumen.",
        )
        parser.add_argument(
            "--tasks-only",
            action="store_true",
            help="Sincroniza solo tareas BL-* y omite épicas e historias.",
        )

    def handle(self, *args, **options):
        backlog_path = Path(options["backlog"])
        map_path = Path(options["map"])
        apply_changes = options["apply"]
        tasks_only = options["tasks_only"]

        items = self.parse_backlog(backlog_path, tasks_only)
        sync_map = self.load_map(map_path)

        if not apply_changes:
            self.print_dry_run(items, sync_map)
            return

        client = self.build_client()
        project_key = self.required_env("JIRA_PROJECT_KEY")

        issue_types = {
            "epic": os.environ.get("JIRA_EPIC_ISSUE_TYPE", "Epic"),
            "story": os.environ.get("JIRA_STORY_ISSUE_TYPE", "Story"),
            "task": os.environ.get("JIRA_TASK_ISSUE_TYPE", "Task"),
        }

        for item in items:
            issue_key = sync_map.get(item["id"])
            fields = self.build_fields(project_key, issue_types[item["kind"]], item)

            if issue_key:
                client.update_issue(issue_key, fields)
                self.stdout.write(f"Actualizado {item['id']} -> {issue_key}")
            else:
                created = client.create_issue(fields)
                issue_key = created["key"]
                sync_map[item["id"]] = issue_key
                self.stdout.write(f"Creado {item['id']} -> {issue_key}")

            self.sync_transition(client, issue_key, item["status"])

        self.save_map(map_path, sync_map)
        self.stdout.write(self.style.SUCCESS("Sincronización completada."))

    def parse_backlog(self, backlog_path, tasks_only):
        if not backlog_path.exists():
            raise CommandError(f"No existe el backlog: {backlog_path}")

        items = []
        current_epic = None
        current_story = None

        for line in backlog_path.read_text(encoding="utf-8").splitlines():
            epic_match = BACKLOG_EPIC_RE.match(line)
            story_match = BACKLOG_STORY_RE.match(line)
            task_match = BACKLOG_TASK_RE.match(line)

            if epic_match:
                current_epic = epic_match.group(1)
                current_story = None

                if not tasks_only:
                    items.append({
                        "id": current_epic,
                        "kind": "epic",
                        "status": "Pendiente",
                        "summary": f"{current_epic} - {epic_match.group(2)}",
                        "description": f"Épica importada desde {backlog_path.name}.",
                    })

            elif story_match:
                current_story = story_match.group(1)

                if not tasks_only:
                    items.append({
                        "id": current_story,
                        "kind": "story",
                        "status": "Pendiente",
                        "summary": f"{current_story} - {story_match.group(2)}",
                        "description": (
                            f"Historia importada desde {backlog_path.name}.\n"
                            f"Épica local: {current_epic or 'Sin épica'}."
                        ),
                    })

            elif task_match:
                backlog_id = task_match.group(1)
                status = task_match.group(2)
                summary = task_match.group(3)

                items.append({
                    "id": backlog_id,
                    "kind": "task",
                    "status": status,
                    "summary": f"{backlog_id} - {summary}",
                    "description": (
                        f"Tarea importada desde {backlog_path.name}.\n"
                        f"Estado local: {status}.\n"
                        f"Épica local: {current_epic or 'Sin épica'}.\n"
                        f"Historia local: {current_story or 'Sin historia'}."
                    ),
                })

        return items

    def print_dry_run(self, items, sync_map):
        self.stdout.write("Modo previsualización. No se llamará a Jira.")
        self.stdout.write(f"Elementos detectados: {len(items)}")

        for item in items:
            issue_key = sync_map.get(item["id"], "nuevo")
            self.stdout.write(
                f"- {item['id']} [{item['status']}] ({item['kind']}) -> {issue_key}: "
                f"{item['summary']}"
            )

        self.stdout.write("")
        self.stdout.write("Ejecuta con --apply para sincronizar con Jira.")

    def build_client(self):
        return JiraClient(
            self.required_env("JIRA_BASE_URL"),
            self.required_env("JIRA_EMAIL"),
            self.required_env("JIRA_API_TOKEN"),
        )

    def build_fields(self, project_key, issue_type, item):
        return {
            "project": {"key": project_key},
            "summary": item["summary"],
            "description": self.to_adf(item["description"]),
            "issuetype": {"name": issue_type},
            "labels": ["backlog-local", item["id"].lower()],
        }

    def sync_transition(self, client, issue_key, local_status):
        target = {
            "Hecho": os.environ.get("JIRA_STATUS_DONE", "Done"),
            "Parcial": os.environ.get("JIRA_STATUS_IN_PROGRESS", "In Progress"),
            "Pendiente": os.environ.get("JIRA_STATUS_TODO", "To Do"),
            "Por revisar": os.environ.get("JIRA_STATUS_REVIEW", ""),
        }.get(local_status, "")

        if not target:
            return

        transitions = client.get_transitions(issue_key)
        transition = next(
            (
                candidate for candidate in transitions
                if candidate["name"].lower() == target.lower()
            ),
            None,
        )

        if transition:
            client.transition_issue(issue_key, transition["id"])
            self.stdout.write(f"Estado actualizado {issue_key} -> {target}")

    def to_adf(self, text):
        paragraphs = []

        for line in text.splitlines():
            paragraphs.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": line or " "}],
            })

        return {
            "type": "doc",
            "version": 1,
            "content": paragraphs,
        }

    def load_map(self, map_path):
        if not map_path.exists():
            return {}

        return json.loads(map_path.read_text(encoding="utf-8"))

    def save_map(self, map_path, sync_map):
        map_path.parent.mkdir(parents=True, exist_ok=True)
        map_path.write_text(
            json.dumps(sync_map, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def required_env(self, name):
        value = os.environ.get(name)

        if not value:
            raise CommandError(f"Falta la variable de entorno {name}.")

        return value
