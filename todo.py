import json
import os

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

    priority = input("Enter priority (High/Medium/Low): ").capitalize()
    due_date = input("Enter due date (optional, e.g. 2026-04-10): ")

    task = {
        "title": title,
        "priority": priority,
        "due_date": due_date if due_date else "No date",
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!")

# View tasks
def view_tasks(tasks):
    if not tasks:
        print("📭 No tasks found.")
        return

    print("\n📋 Your Tasks:\n")
    for i, task in enumerate(tasks):
        status = "✔" if task["completed"] else "✘"
        print(f"{i+1}. {task['title']} [{task['priority']}] | Due: {task['due_date']} | {status}")

# Delete task
def delete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if index < 0 or index >= len(tasks):
            raise ValueError
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"🗑 Deleted: {removed['title']}")
    except:
        print("❌ Invalid input!")

# Complete task
def complete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to mark complete: ")) - 1
        if index < 0 or index >= len(tasks):
            raise ValueError
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("✅ Task marked as completed!")
    except:
        print("❌ Invalid input!")

# Search task
def search_task(tasks):
    keyword = input("Enter keyword to search: ").lower()
    found = False

    for i, task in enumerate(tasks):
        if keyword in task["title"].lower():
            status = "✔" if task["completed"] else "✘"
            print(f"{i+1}. {task['title']} [{task['priority']}] | {status}")
            found = True

    if not found:
        print("❌ No matching tasks found.")

# Menu
def main():
    tasks = load_tasks()

    while True:
        print("\n===== 🚀 TO-DO LIST MENU =====")
        print("1. Add Task (add)")
        print("2. View Tasks (view)")
        print("3. Delete Task (delete)")
        print("4. Mark Completed (complete)")
        print("5. Search Task (search)")
        print("6. Exit (exit)")

        choice = input("Enter your choice: ").lower().strip()

        if choice in ["1", "add"]:
            add_task(tasks)
        elif choice in ["2", "view"]:
            view_tasks(tasks)
        elif choice in ["3", "delete"]:
            delete_task(tasks)
        elif choice in ["4", "complete"]:
            complete_task(tasks)
        elif choice in ["5", "search"]:
            search_task(tasks)
        elif choice in ["6", "exit"]:
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main()