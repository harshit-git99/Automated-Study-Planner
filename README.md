# 📚 AI-Powered Study Planner & Deadline Manager

An intelligent LLM-based study planner that helps students manage tasks,
deadlines, and generate optimized daily study schedules using AI.

------------------------------------------------------------------------

## 🚀 Features

-   Add, view, and manage study tasks
-   Priority-based scheduling
-   Deadline-aware planning
-   Burnout-prevention balanced schedules
-   AI-generated daily study plans
-   CLI-based simple interface
-   JSON-based local storage

------------------------------------------------------------------------

## 🧠 Tech Stack

-   Python 3.8+
-   OpenAI API (or any LLM API)
-   Rich (for beautiful CLI output)
-   JSON (local storage)

------------------------------------------------------------------------

## 📁 Project Structure

    study_planner_ai/
    │
    ├── main.py        # CLI interface
    ├── planner.py     # Core AI planning logic
    ├── llm.py         # LLM communication
    ├── database.py    # Local task storage
    └── tasks.json     # Auto-created task database

------------------------------------------------------------------------

## 🔧 Installation

1.  Clone or download this project
2.  Install dependencies:

``` bash
pip install openai python-dotenv rich
```

3.  Set your OpenAI API key:

**Linux/Mac**

``` bash
export OPENAI_API_KEY="your_api_key_here"
```

**Windows**

``` bash
setx OPENAI_API_KEY "your_api_key_here"
```

------------------------------------------------------------------------

## ▶️ How to Run (CLI)

``` bash
python main.py
```

------------------------------------------------------------------------

## 🌐 How to Run (Web UI)

This launches a small Flask server and serves the static frontend.

1) Install deps:

```bash
pip install -r requirements.txt
```

2) (Optional) set your OpenAI key to enable AI-generated plans:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

3) Start the web app:

```bash
python web_app.py
```

4) Open:

- http://127.0.0.1:5000

------------------------------------------------------------------------

## 📝 Usage


### Add Task

Enter: - Subject - Task description - Deadline (YYYY-MM-DD) - Priority
(High/Medium/Low) - Estimated hours

### Generate AI Study Plan

The AI will: - Analyze your workload - Sort by deadlines - Balance your
schedule - Prevent overload - Output a day-wise plan

------------------------------------------------------------------------

## 💡 Example Output

    Monday:
    - Math: Algebra practice (2 hrs)
    - Physics: Chapter 3 notes (1.5 hrs)

    Tuesday:
    - Chemistry: Organic reactions (2 hrs)
    ...

------------------------------------------------------------------------

## 🔒 Data Storage

All tasks are saved locally in:

    tasks.json

------------------------------------------------------------------------

## 📈 Future Upgrades

-   Google Calendar sync
-   WhatsApp reminders
-   Pomodoro timer
-   Web dashboard
-   Mobile version
-   PDF export
-   Exam-mode planner
-   Stress-aware scheduling

------------------------------------------------------------------------

## 🧑‍💻 Author

Built with ❤️ by Harshit

------------------------------------------------------------------------

## ⚠️ Disclaimer

This tool provides AI-based suggestions. Always review schedules
manually.

------------------------------------------------------------------------

Happy Studying! 🎯
