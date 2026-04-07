import tkinter as tk
from tkinter import messagebox

# File to store tasks
FILE_NAME = "tasks.txt"

# Load tasks from file
def load_tasks():
    try:
        with open(FILE_NAME, "r") as file:
            tasks = file.readlines()
            for task in tasks:
                listbox.insert(tk.END, task.strip())
    except FileNotFoundError:
        pass

# Save tasks to file
def save_tasks():
    tasks = listbox.get(0, tk.END)
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")

# Add task
def add_task():
    task = entry.get()
    if task != "":
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter a task")

# Delete task
def delete_task():
    try:
        selected = listbox.curselection()[0]
        listbox.delete(selected)
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task to delete")

# Main window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x400")

# Entry box
entry = tk.Entry(root, width=30, font=("Arial", 14))
entry.pack(pady=10)

# Buttons
add_btn = tk.Button(root, text="Add Task", command=add_task, width=15)
add_btn.pack(pady=5)

del_btn = tk.Button(root, text="Delete Task", command=delete_task, width=15)
del_btn.pack(pady=5)

# Listbox
listbox = tk.Listbox(root, width=40, height=15)
listbox.pack(pady=10)

# Load saved tasks
load_tasks()

# Run app
root.mainloop()