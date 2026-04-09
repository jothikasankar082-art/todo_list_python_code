import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

FILE_NAME = "tasks.json"

# ------------------ Data Handling ------------------
def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
            for task in data:
                tree.insert("", "end", values=(
                    task["text"], task["priority"], task["time"], task["status"]
                ))
    except:
        pass

def save_tasks():
    tasks = []
    for item in tree.get_children():
        val = tree.item(item)["values"]
        tasks.append({
            "text": val[0],
            "priority": val[1],
            "time": val[2],
            "status": val[3]
        })
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# ------------------ Functions ------------------
def add_task():
    text = entry.get()
    priority = priority_box.get()
    if text:
        now = datetime.now().strftime("%d-%m-%Y %H:%M")
        tree.insert("", "end", values=(text, priority, now, "Pending"))
        entry.delete(0, tk.END)
        save_tasks()
        update_count()
    else:
        messagebox.showwarning("Warning", "Enter task!")

def delete_task():
    selected = tree.selection()
    if selected:
        for item in selected:
            tree.delete(item)
        save_tasks()
        update_count()

def mark_done():
    selected = tree.selection()
    for item in selected:
        vals = tree.item(item)["values"]
        tree.item(item, values=(vals[0], vals[1], vals[2], "Done"))
    save_tasks()
    update_count()

def search_task():
    query = search_entry.get().lower()
    for item in tree.get_children():
        text = tree.item(item)["values"][0].lower()
        if query in text:
            tree.selection_set(item)

def update_count():
    total = len(tree.get_children())
    done = sum(1 for i in tree.get_children() if tree.item(i)["values"][3] == "Done")
    status_label.config(text=f"✔ Done: {done} / {total}")

def suggest_task():
    suggestions = [
        "Drink water 💧",
        "Take a short walk 🚶",
        "Check emails 📧",
        "Revise your notes 📚",
        "Plan tomorrow 📅"
    ]
    messagebox.showinfo("Suggestion", suggestions[datetime.now().second % len(suggestions)])

# ------------------ UI ------------------
root = tk.Tk()
root.title("Smart To-Do Dashboard")
root.geometry("700x550")
root.config(bg="#121212")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#1e1e1e",
                foreground="white",
                rowheight=28,
                fieldbackground="#1e1e1e",
                font=("Segoe UI", 10))

style.map("Treeview", background=[("selected", "#00adb5")])

# Title
tk.Label(root, text="🚀 Smart Task Dashboard",
         bg="#121212", fg="#00adb5",
         font=("Segoe UI", 22, "bold")).pack(pady=10)

# Input Frame
frame = tk.Frame(root, bg="#121212")
frame.pack()

entry = tk.Entry(frame, width=25, font=("Segoe UI", 12))
entry.grid(row=0, column=0, padx=5)

priority_box = ttk.Combobox(frame, values=["High", "Medium", "Low"], width=10)
priority_box.set("Medium")
priority_box.grid(row=0, column=1, padx=5)

ttk.Button(frame, text="Add Task", command=add_task).grid(row=0, column=2, padx=5)

# Search
search_entry = tk.Entry(root, width=30)
search_entry.pack(pady=5)
ttk.Button(root, text="Search", command=search_task).pack()

# Treeview
columns = ("Task", "Priority", "Time", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack()

ttk.Button(btn_frame, text="Mark Done", command=mark_done).grid(row=0, column=0, padx=5)
ttk.Button(btn_frame, text="Delete", command=delete_task).grid(row=0, column=1, padx=5)
ttk.Button(btn_frame, text="💡 Suggest", command=suggest_task).grid(row=0, column=2, padx=5)

# Status
status_label = tk.Label(root, text="", bg="#121212", fg="white", font=("Segoe UI", 12))
status_label.pack(pady=10)

# Load Data
load_tasks()
update_count()

root.mainloop()