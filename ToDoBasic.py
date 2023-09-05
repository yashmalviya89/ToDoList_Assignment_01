import argparse
import csv
import os
import re
from datetime import datetime

# Function to read tasks from the CSV file
def read_tasks():
    tasks = {}
    if not os.path.exists('tasks.csv'):
        with open('tasks.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Title', 'Created At', 'Completed At', 'Status'])
    else:
        with open('tasks.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                task_id, title, created_at, completed_at, status = row
                tasks[task_id] = [title, created_at, completed_at, status]
    return tasks

# Function to write tasks to the CSV file
def write_tasks(tasks):
    with open('tasks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Title', 'Created At', 'Completed At', 'Status'])
        for task_id, task_details in tasks.items():
            writer.writerow([task_id] + task_details)

# Function to create a new task
def create_task(title, status='incomplete'):
    tasks = read_tasks()

    # Check if there's a task with the same title and the same status
    for task_id, task_details in tasks.items():
        if task_details[0] == title and task_details[3] == status:
            print(f"Task with the same title '{title}' already exists with the incomplete status.")
            return

    # Generate a new unique task_id by finding the first available ID
    task_id = str(1)
    while task_id in tasks:
        task_id = str(int(task_id) + 1)

    created_at = str(datetime.now())
    tasks[task_id] = [title, created_at, '', status]

    write_tasks(tasks)
    print("Task created successfully.")

# Function to edit a task's title
def edit_title(task_id, new_title):
    tasks = read_tasks()
    if task_id in tasks:
        tasks[task_id][0] = new_title
        write_tasks(tasks)
        print("Task title updated successfully.")
    else:
        print("Task not found.")

# Function to mark a task as complete
def mark_complete(task_id):
    tasks = read_tasks()
    if task_id in tasks:
        tasks[task_id][2] = str(datetime.now())
        tasks[task_id][3] = 'complete'
        write_tasks(tasks)
        print("Task marked as complete.")
    else:
        print("Task not found.")

# Function to delete a task
def delete_task(task_id):
    tasks = read_tasks()
    if task_id in tasks:
        del tasks[task_id]
        write_tasks(tasks)
        print("Task deleted successfully.")
    else:
        print("Task not found.")

# Function to list tasks
def list_tasks(status=None):
    tasks = read_tasks()
    for task_id, task_details in tasks.items():
        if not status or task_details[3] == status:
            print(f"ID: {task_id}, Title: {task_details[0]}, Status: {task_details[3]}")

def search_task(title):
    tasks = read_tasks()
    for task_id, task_details in tasks.items():
        if re.search(title, task_details[0]):
            print(f"ID: {task_id}, Title: {task_details[0]}, Status: {task_details[3]}")

# Main function to handle user input
def main():
    parser = argparse.ArgumentParser(description="TODO List Manager")
    parser.add_argument('--create', help="Create a new task with title")
    parser.add_argument('--edit-title', nargs=2, help="Edit task title. Provide task ID and new title")
    parser.add_argument('--mark-complete', help="Mark a task as complete. Provide task ID")
    parser.add_argument('--delete', help="Delete a task. Provide task ID")
    parser.add_argument('--list', choices=['all', 'incomplete', 'complete'], help="List tasks")
    parser.add_argument('--search', help="Search tasks by title")
    args = parser.parse_args()

    if args.create:
        create_task(args.create)
    elif args.edit_title:
        task_id, new_title = args.edit_title
        edit_title(task_id, new_title)
    elif args.mark_complete:
        mark_complete(args.mark_complete)
    elif args.delete:
        delete_task(args.delete)
    elif args.list:
        if args.list == 'all':
            list_tasks()
        else:
            list_tasks(args.list)
    elif args.search:
        search_task(args.search)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
