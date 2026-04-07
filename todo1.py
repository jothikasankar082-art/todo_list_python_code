import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "tasks.txt"

# ---------- Functions ----------
def load_tasks():
    try:
        with open(FILE_NAME, "r") as file:
            for task in file.readlines():
                listbox.insert("", "end", values=(task.strip(),))
    except FileNotFoundError:
        pass

def save_tasks():
    tasks = listbox.get_children()
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(listbox.item(task)['values'][0] + "\n")

def add_task():
    task = entry.get()
    if task:
        listbox.insert("", "end", values=(task,))
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter a task")

def delete_task():
    selected = listbox.selection()
    if selected:
        for item in selected:
            listbox.delete(item)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to delete")

# ---------- Main Window ----------
root = tk.Tk()
root.title("✨ To-Do List")
root.geometry("450x500")
root.configure(bg="#1e1e2f")

# ---------- Style ----------
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#2b2b3c",
                foreground="white",
                rowheight=30,
                fieldbackground="#2b2b3c",
                font=("Segoe UI", 11))

style.map("Treeview", background=[("selected", "#4e73df")])

style.configure("TButton",
                font=("Segoe UI", 10, "bold"),
                padding=6)

# ---------- Title ----------
title = tk.Label(root, text="📝 My Tasks",
                 bg="#1e1e2f",
                 fg="white",
                 font=("Segoe UI", 20, "bold"))
title.pack(pady=10)

# ---------- Input Frame ----------
frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

entry = tk.Entry(frame, width=25, font=("Segoe UI", 12))
entry.grid(row=0, column=0, padx=5)

add_btn = ttk.Button(frame, text="Add", command=add_task)
add_btn.grid(row=0, column=1, padx=5)

# ---------- List Frame ----------
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = ttk.Treeview(list_frame, columns=("Task",), show="headings", height=12)
listbox.heading("Task", text="Your Tasks")
listbox.pack()

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# ---------- Delete Button ----------
del_btn = ttk.Button(root, text="Delete Selected", command=delete_task)
del_btn.pack(pady=10)

# ---------- Load Data ----------
load_tasks()

# ---------- Run ----------
root.mainloop()