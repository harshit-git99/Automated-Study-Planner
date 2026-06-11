from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


PRIORITY_WEIGHT = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


def _parse_date(date_str: str) -> dt.date:
    return dt.datetime.strptime(date_str, "%Y-%m-%d").date()


def _today() -> dt.date:
    return dt.date.today()


def score_task(task: Dict[str, Any]) -> Tuple[int, dt.date]:
    # Higher priority first; earlier deadlines first.
    priority = str(task.get("priority", "Low"))
    p = PRIORITY_WEIGHT.get(priority, 1)
    deadline = _parse_date(task["deadline"])
    # negative priority for descending behavior with python sort ascending.
    return (-p, deadline)


def build_schedule(tasks: List[Dict[str, Any]], *, max_hours_per_day: float = 4.0) -> Dict[str, List[Dict[str, Any]]]:
    """Greedy heuristic: allocate tasks into day buckets until deadlines.

    Returns: {"YYYY-MM-DD": [{task fields + "allocated_hours"}, ...]}
    """
    if not tasks:
        return {}

    tasks_sorted = sorted(tasks, key=score_task)

    schedule: Dict[str, List[Dict[str, Any]]] = {}

    start_date = _today()

    # We'll iterate through days up to the latest deadline.
    latest_deadline = max(_parse_date(t["deadline"]) for t in tasks_sorted)
    day = start_date

    # remaining hours per task
    remaining = {id(t): float(t.get("estimated_hours", 0) or 0) for t in tasks_sorted}
    task_by_id = {id(t): t for t in tasks_sorted}

    # For each day, pick the most urgent remaining tasks that haven't passed their deadline.
    while day <= latest_deadline:
        day_str = day.isoformat()
        schedule.setdefault(day_str, [])
        used = 0.0

        # Candidate tasks: deadlines >= current day and still remaining.
        candidates = []
        for tid, t in task_by_id.items():
            rem = remaining[tid]
            if rem <= 0:
                continue
            deadline = _parse_date(t["deadline"])
            if deadline < day:
                continue
            priority = PRIORITY_WEIGHT.get(str(t.get("priority", "Low")), 1)
            candidates.append((deadline, -priority, tid))

        # Sort by earliest deadline, then higher priority.
        candidates.sort(key=lambda x: (x[0], x[1]))

        for _, _, tid in candidates:
            if used >= max_hours_per_day:
                break
            t = task_by_id[tid]
            rem = remaining[tid]
            if rem <= 0:
                continue
            alloc = min(rem, max_hours_per_day - used)
            if alloc <= 0:
                continue

            schedule[day_str].append(
                {
                    "subject": t["subject"],
                    "description": t["description"],
                    "deadline": t["deadline"],
                    "priority": t["priority"],
                    "estimated_hours": t.get("estimated_hours", alloc),
                    "allocated_hours": round(alloc, 2),
                }
            )
            remaining[tid] = round(rem - alloc, 6)
            used += alloc

        day = day + dt.timedelta(days=1)

    # Remove empty days
    schedule = {k: v for k, v in schedule.items() if v}
    return schedule


def format_prompt(tasks: List[Dict[str, Any]], schedule: Dict[str, List[Dict[str, Any]]], *, max_days: int = 14) -> str:
    sorted_days = sorted(schedule.keys())[:max_days]

    lines = []
    lines.append("Create a day-wise study plan based on the tasks and the schedule constraints.")
    lines.append("")
    lines.append("Tasks:")
    if tasks:
        for t in sorted(tasks, key=score_task):
            lines.append(
                f"- {t['subject']}: {t['description']} | deadline={t['deadline']} | priority={t['priority']} | est_hours={t['estimated_hours']}"
            )

    lines.append("")
    lines.append("Planned allocation by day (allocated_hours):")
    for day in sorted_days:
        lines.append(f"\n{day}:")
        for item in schedule[day]:
            lines.append(
                f"- {item['subject']}: {item['description']} ({item['allocated_hours']} hrs)"
            )

    lines.append("")
    lines.append(
        "Guidelines:\n"
        "1) Keep each day realistic.\n"
        "2) Add short focus blocks (e.g., 45-60 min) and 5-10 min breaks conceptually.\n"
        "3) Include 1 light review/revision item when possible to reduce stress.\n"
        "4) Output only the final schedule, grouped by day."
    )

    return "\n".join(lines)

