import sqlite3
import os

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "tasks.db")

# Ensure the folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    """Initialize the database and create the tasks table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def add_task(task):
    """Add a new task to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        return "Task added!"
    except sqlite3.Error as e:
        return f"Error adding task: {e}"
    finally:
        conn.close()

def show_tasks():
    """Return all tasks as a formatted string."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT task FROM tasks")
        tasks = cur.fetchall()
        if tasks:
            return "\n".join([f"- {t[0]}" for t in tasks])
        return "No tasks yet."
    except sqlite3.Error as e:
        return f"Error fetching tasks: {e}"
    finally:
        conn.close()

# Initialize DB automatically when this module is imported
init_db()
