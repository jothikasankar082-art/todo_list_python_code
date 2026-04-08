import json
import os

FILE_NAME = "tasks.json"

# Load tasks from file
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

# Save tasks to file
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# Add a task
def add_task(tasks):
    title = input("Enter task title: ")
    priority = input("Enter priority (High/Medium/Low): ")
    
    task = {
        "title": title,
        "priority": priority,
        "completed": False
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!")

# View tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    
    print("\n📋 Your Tasks:\n")
    for i, task in enumerate(tasks):
        status = "✔" if task["completed"] else "✘"
        print(f"{i+1}. {task['title']} [{task['priority']}] - {status}")

# Delete task
def delete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"🗑 Deleted: {removed['title']}")
    except:
        print("Invalid input!")

# Mark task as completed
def complete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to mark complete: ")) - 1
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("✅ Task marked as completed!")
    except:
        print("Invalid input!")

# Main menu
def main():
    tasks = load_tasks()
    
    while True:
        print("\n===== TO-DO LIST MENU =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Mark Task as Completed")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()