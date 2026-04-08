import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"

# Load tasks
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

# Save tasks
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# Add task
def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print("❌ Task cannot be empty!")
        return

    priority = input("Priority (High/Medium/Low): ").capitalize()
    category = input("Category (Work/Personal/Study): ").capitalize()
    due_date = input("Due date (YYYY-MM-DD): ")

    task = {
        "title": title,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added!")

# Check overdue
def is_overdue(due_date):
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        return due < datetime.now()
    except:
        return False

# View tasks
def view_tasks(tasks):
    if not tasks:
        print("📭 No tasks found.")
        return

    print("\n📋 TASK LIST:\n")
    for i, task in enumerate(tasks):
        status = "✔" if task["completed"] else "✘"
        overdue = "⚠ OVERDUE" if not task["completed"] and is_overdue(task["due_date"]) else ""
        
        print(f"{i+1}. {task['title']}")
        print(f"   Priority: {task['priority']} | Category: {task['category']}")
        print(f"   Due: {task['due_date']} {overdue}")
        print(f"   Status: {status}\n")

# Complete task
def complete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number: ")) - 1
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("✅ Task completed!")
    except:
        print("❌ Invalid input!")

# Delete task
def delete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number: ")) - 1
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"🗑 Deleted: {removed['title']}")
    except:
        print("❌ Invalid input!")

# Edit task
def edit_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to edit: ")) - 1
        task = tasks[index]

        print("Leave blank to keep old value")

        new_title = input(f"New title ({task['title']}): ") or task['title']
        new_priority = input(f"New priority ({task['priority']}): ") or task['priority']
        new_category = input(f"New category ({task['category']}): ") or task['category']
        new_due = input(f"New due date ({task['due_date']}): ") or task['due_date']

        task.update({
            "title": new_title,
            "priority": new_priority,
            "category": new_category,
            "due_date": new_due
        })

        save_tasks(tasks)
        print("✏️ Task updated!")

    except:
        print("❌ Invalid input!")

# Search
def search_task(tasks):
    keyword = input("Search keyword: ").lower()
    found = False

    for i, task in enumerate(tasks):
        if keyword in task["title"].lower():
            print(f"{i+1}. {task['title']} ({task['priority']})")
            found = True

    if not found:
        print("❌ No results found.")

# Progress
def show_progress(tasks):
    if not tasks:
        print("No tasks yet.")
        return

    completed = sum(1 for t in tasks if t["completed"])
    total = len(tasks)
    percent = (completed / total) * 100

    print(f"📊 Progress: {completed}/{total} tasks completed ({percent:.2f}%)")

# Sort tasks
def sort_tasks(tasks):
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: priority_order.get(x["priority"], 4))
    save_tasks(tasks)
    print("🔽 Tasks sorted by priority!")

# Menu
def main():
    tasks = load_tasks()

    while True:
        print("\n===== 🚀 ADVANCED TO-DO =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Edit Task")
        print("6. Search Task")
        print("7. Show Progress")
        print("8. Sort by Priority")
        print("9. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            search_task(tasks)
        elif choice == "7":
            show_progress(tasks)
        elif choice == "8":
            sort_tasks(tasks)
        elif choice == "9":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()