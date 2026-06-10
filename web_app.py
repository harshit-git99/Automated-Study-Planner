import os
from typing import Any, Dict, List

from flask import Flask, jsonify, request, send_from_directory

from study_planner_ai.database import Task, add_task, clear_tasks, load_tasks
from study_planner_ai.llm import LLMClient
from study_planner_ai.planner import build_schedule, format_prompt


def create_app() -> Flask:
    app = Flask(__name__, static_folder="frontend", static_url_path="")

    @app.get("/api/tasks")
    def api_get_tasks():
        return jsonify({"tasks": load_tasks()})

    @app.post("/api/tasks")
    def api_add_task():
        payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}

        required = ["subject", "description", "deadline", "priority", "estimated_hours"]
        missing = [k for k in required if k not in payload]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        try:
            task = Task(
                subject=str(payload["subject"]).strip(),
                description=str(payload["description"]).strip(),
                deadline=str(payload["deadline"]).strip(),
                priority=str(payload["priority"]).strip().capitalize(),
                estimated_hours=float(payload["estimated_hours"]),
            )
        except Exception as e:
            return jsonify({"error": f"Invalid input: {e}"}), 400

        add_task(task)
        return jsonify({"ok": True, "tasks": load_tasks()})

    @app.delete("/api/tasks")
    def api_clear_tasks():
        clear_tasks()
        return jsonify({"ok": True})

    @app.post("/api/plan")
    def api_generate_plan():
        tasks: List[Dict[str, Any]] = load_tasks()
        if not tasks:
            return jsonify({"error": "No tasks found. Add at least one task."}), 400

        payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
        max_hours_per_day = float(payload.get("max_hours_per_day", 4.0))

        schedule = build_schedule(tasks, max_hours_per_day=max_hours_per_day)
        prompt = format_prompt(tasks, schedule)

        # If OPENAI_API_KEY is not configured, fall back to heuristic schedule.
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            out_lines: List[str] = []
            for day in sorted(schedule.keys()):
                out_lines.append(f"{day}:")
                for item in schedule[day]:
                    out_lines.append(
                        f"- {item['subject']}: {item['description']} ({item['allocated_hours']} hrs)"
                    )
            return jsonify({"plan": "\n".join(out_lines).strip(), "used_llm": False})

        try:
            llm = LLMClient()
            plan = llm.generate_study_plan(prompt)
            return jsonify({"plan": plan, "used_llm": True})
        except Exception:
            # LLM failed -> fallback.
            out_lines: List[str] = []
            for day in sorted(schedule.keys()):
                out_lines.append(f"{day}:")
                for item in schedule[day]:
                    out_lines.append(
                        f"- {item['subject']}: {item['description']} ({item['allocated_hours']} hrs)"
                    )
            return jsonify({"plan": "\n".join(out_lines).strip(), "used_llm": False})

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/static/<path:filename>")
    def static_files(filename: str):
        return send_from_directory(app.static_folder, filename)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)

