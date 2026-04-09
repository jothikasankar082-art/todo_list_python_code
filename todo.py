import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry

# ---------------- DATABASE ----------------
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    priority TEXT,
    due_date TEXT,
    status TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def add_task():
    text = task_entry.get()
    priority = priority_box.get()
    due = cal.get_date()

    if text:
        cursor.execute("INSERT INTO tasks(text, priority, due_date, status) VALUES (?, ?, ?, ?)",
                       (text, priority, str(due), "Pending"))
        conn.commit()
        load_tasks()
        update_dashboard()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Enter a task")

def load_tasks():
    for i in tree.get_children():
        tree.delete(i)

    cursor.execute("SELECT * FROM tasks")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def mark_done():
    selected = tree.selection()
    for item in selected:
        task_id = tree.item(item)["values"][0]
        cursor.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()
    load_tasks()
    update_dashboard()

def delete_task():
    selected = tree.selection()
    for item in selected:
        task_id = tree.item(item)["values"][0]
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    load_tasks()
    update_dashboard()

def update_dashboard():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='Done'")
    done = cursor.fetchone()[0]

    percent = (done / total * 100) if total else 0

    progress['value'] = percent
    stats_label.config(text=f"Completed: {done}/{total} ({int(percent)}%)")

def suggest():
    cursor.execute("SELECT priority, COUNT(*) FROM tasks GROUP BY priority")
    data = cursor.fetchall()

    if not data:
        msg = "Start by adding tasks!"
    else:
        msg = "Focus on HIGH priority tasks first 🚀"

    messagebox.showinfo("AI Suggestion", msg)

def search_task():
    query = search_entry.get()
    for i in tree.get_children():
        tree.delete(i)

    cursor.execute("SELECT * FROM tasks WHERE text LIKE ?", ('%'+query+'%',))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# ---------------- UI ----------------
root = tk.Tk()
root.title("AI Productivity Dashboard")
root.geometry("900x600")
root.config(bg="#121212")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#1e1e1e",
                foreground="white",
                fieldbackground="#1e1e1e",
                rowheight=30)

style.map("Treeview", background=[("selected", "#00adb5")])

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# -------- Dashboard Tab --------
dashboard = tk.Frame(notebook, bg="#121212")
notebook.add(dashboard, text="Dashboard")

tk.Label(dashboard, text="📊 Productivity Overview",
         bg="#121212", fg="#00adb5",
         font=("Segoe UI", 20, "bold")).pack(pady=20)

progress = ttk.Progressbar(dashboard, length=400)
progress.pack(pady=10)

stats_label = tk.Label(dashboard, text="", bg="#121212", fg="white",
                       font=("Segoe UI", 14))
stats_label.pack()

ttk.Button(dashboard, text="💡 Get Suggestion", command=suggest).pack(pady=20)

# -------- Tasks Tab --------
tasks_tab = tk.Frame(notebook, bg="#121212")
notebook.add(tasks_tab, text="Tasks")

# Input
top_frame = tk.Frame(tasks_tab, bg="#121212")
top_frame.pack(pady=10)

task_entry = tk.Entry(top_frame, width=30)
task_entry.grid(row=0, column=0, padx=5)

priority_box = ttk.Combobox(top_frame, values=["High", "Medium", "Low"])
priority_box.set("Medium")
priority_box.grid(row=0, column=1)

cal = DateEntry(top_frame)
cal.grid(row=0, column=2, padx=5)

ttk.Button(top_frame, text="Add", command=add_task).grid(row=0, column=3)

# Search
search_entry = tk.Entry(tasks_tab)
search_entry.pack(pady=5)
ttk.Button(tasks_tab, text="Search", command=search_task).pack()

# Table
cols = ("ID", "Task", "Priority", "Due", "Status")
tree = ttk.Treeview(tasks_tab, columns=cols, show="headings")

for col in cols:
    tree.heading(col, text=col)

tree.pack(fill="both", expand=True)

# Buttons
btn_frame = tk.Frame(tasks_tab, bg="#121212")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Done", command=mark_done).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Delete", command=delete_task).grid(row=0, column=1, padx=5)

# -------- Analytics Tab --------
analytics = tk.Frame(notebook, bg="#121212")
notebook.add(analytics, text="Analytics")

tk.Label(analytics, text="📈 Analytics Coming Soon...",
         bg="#121212", fg="white",
         font=("Segoe UI", 18)).pack(pady=50)

# Load initial data
load_tasks()
update_dashboard()

root.mainloop()