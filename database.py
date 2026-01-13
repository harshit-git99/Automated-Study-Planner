import json
from datetime import datetime

DB_FILE = "tasks.json"

def load_tasks():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(DB_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
