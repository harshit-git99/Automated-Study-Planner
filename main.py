from database import load_tasks, save_tasks
from planner import generate_plan
from datetime import datetime
from rich import print

def add_task():
    subject = input("Subject: ")
    task = input("Task Description: ")
    deadline = input("Deadline (YYYY-MM-DD): ")
    priority = input("Priority (High/Medium/Low): ")
    hours = input("Estimated hours: ")

    tasks = load_tasks()

    tasks.append({
        "subject": subject,
        "task": task,
        "deadline": deadline,
        "priority": priority,
        "hours": hours
    })

    save_tasks(tasks)
    print("[green]Task added successfully![/green]")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("[yellow]No tasks found[/yellow]")
        return

    for i, t in enumerate(tasks):
        print(f"{i+1}. {t['subject']} - {t['task']} | Due: {t['deadline']} | Priority: {t['priority']}")

def generate_study_plan():
    tasks = load_tasks()
    if not tasks:
        print("[red]No tasks to plan[/red]")
        return

    plan = generate_plan(tasks)
    print("\n[bold cyan]Your AI-Generated Study Plan:[/bold cyan]\n")
    print(plan)

def main():
    while True:
        print("\n[bold]AI Study Planner[/bold]")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Generate Study Plan")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            generate_study_plan()
        elif choice == "4":
            break
        else:
            print("[red]Invalid choice[/red]")

if __name__ == "__main__":
    main()
