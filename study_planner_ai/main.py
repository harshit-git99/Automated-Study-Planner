import sys
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .database import Task, add_task, clear_tasks, load_tasks
from .llm import LLMClient
from .planner import build_schedule, format_prompt


console = Console()


def _prompt_str(msg: str) -> str:
    return input(msg).strip()


def _prompt_float(msg: str) -> float:
    while True:
        raw = input(msg).strip()
        try:
            return float(raw)
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")


def _prompt_priority(msg: str = "Priority (High/Medium/Low): ") -> str:
    while True:
        p = input(msg).strip().capitalize()
        if p in {"High", "Medium", "Low"}:
            return p
        console.print("[red]Priority must be High, Medium, or Low.[/red]")


def view_tasks(tasks: List[Dict[str, Any]]) -> None:
    if not tasks:
        console.print(Panel("No tasks found.", title="Tasks"))
        return

    table = Table(title="Saved Study Tasks", show_lines=False)
    table.add_column("Subject")
    table.add_column("Deadline")
    table.add_column("Priority")
    table.add_column("Est. Hours", justify="right")
    table.add_column("Description")

    for t in tasks:
        table.add_row(
            str(t.get("subject", "")),
            str(t.get("deadline", "")),
            str(t.get("priority", "")),
            str(t.get("estimated_hours", "")),
            str(t.get("description", "")),
        )

    console.print(table)


def add_task_flow() -> None:
    subject = _prompt_str("Subject: ")
    description = _prompt_str("Task description: ")
    deadline = _prompt_str("Deadline (YYYY-MM-DD): ")
    priority = _prompt_priority()
    estimated_hours = _prompt_float("Estimated hours: ")

    task = Task(
        subject=subject,
        description=description,
        deadline=deadline,
        priority=priority,
        estimated_hours=estimated_hours,
    )
    add_task(task)
    console.print(Panel("Task added successfully!", title="Success", style="green"))


def generate_plan_flow() -> None:
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]Add at least one task before generating a plan.[/yellow]")
        return

    # Basic knobs (kept simple for CLI).
    max_hours_per_day = 4.0
    schedule = build_schedule(tasks, max_hours_per_day=max_hours_per_day)
    if not schedule:
        console.print("[yellow]Could not build a schedule from current tasks.[/yellow]")
        return

    prompt = format_prompt(tasks, schedule)

    console.print(Panel("Generating AI plan... (this may take a moment)", title="AI"))
    try:
        llm = LLMClient()
        plan = llm.generate_study_plan(prompt)
    except Exception as e:
        console.print(f"[red]Failed to generate AI plan:[/red] {e}")
        console.print("[yellow]Showing heuristic schedule instead.[/yellow]")
        # Fallback: show the planned schedule (grouped by day)
        out_lines = []
        for day in sorted(schedule.keys()):
            out_lines.append(f"\n{day}:")
            for item in schedule[day]:
                out_lines.append(f"- {item['subject']}: {item['description']} ({item['allocated_hours']} hrs)")
        plan = "\n".join(out_lines).strip()

    console.print(Panel(plan, title="Your AI Study Plan", subtitle=f"Max {max_hours_per_day} hrs/day", width=100))



def main() -> None:
    console.print(Panel("AI-Powered Study Planner", subtitle="Manage tasks + generate day-wise plans", width=100))

    while True:
        console.print(
            "\n[bold]Menu[/bold]\n"
            "1) Add Task\n"
            "2) View Tasks\n"
            "3) Generate AI Study Plan\n"
            "4) Clear All Tasks\n"
            "5) Exit"
        )

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            add_task_flow()
        elif choice == "2":
            view_tasks(load_tasks())
        elif choice == "3":
            generate_plan_flow()
        elif choice == "4":
            confirm = input("Type YES to clear all tasks: ").strip().upper()
            if confirm == "YES":
                clear_tasks()
                console.print(Panel("All tasks cleared.", title="Done", style="green"))
            else:
                console.print("[yellow]Canceled.[/yellow]")
        elif choice == "5":
            console.print("Goodbye! 👋")
            return
        else:
            console.print("[red]Invalid option. Please choose 1-5.[/red]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted.[/red]")
        sys.exit(1)

