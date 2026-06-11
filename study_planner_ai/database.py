import json
import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    subject: str
    description: str
    deadline: str  # YYYY-MM-DD
    priority: str  # High/Medium/Low
    estimated_hours: float


def _default_tasks_path() -> str:
    # Keep tasks.json alongside the package for easy discovery.
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "tasks.json")


def load_tasks(tasks_path: Optional[str] = None) -> List[Dict[str, Any]]:
    path = tasks_path or _default_tasks_path()
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Support either {"tasks": [...]} or [...] formats.
    if isinstance(data, dict) and "tasks" in data:
        return data["tasks"]
    if isinstance(data, list):
        return data

    return []


def save_tasks(tasks: List[Dict[str, Any]], tasks_path: Optional[str] = None) -> None:
    path = tasks_path or _default_tasks_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    payload = {"tasks": tasks}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def add_task(task: Task, tasks_path: Optional[str] = None) -> None:
    tasks = load_tasks(tasks_path)
    tasks.append(asdict(task))
    save_tasks(tasks, tasks_path)


def clear_tasks(tasks_path: Optional[str] = None) -> None:
    save_tasks([], tasks_path)

