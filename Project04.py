
'''To-Do List CLI based on python

Save tasks in a .txt file or use SQLite in a db database. '''




import sqlite3
import os
from datetime import datetime

class ToDoList:
    def __init__(self, storage_type='txt'):
        """Initialize the ToDoList with either text file or SQLite database storage"""
        self.storage_type = storage_type
        self.tasks = []
        
        if self.storage_type == 'db':
            self.conn = sqlite3.connect('todo.db')
            self.cursor = self.conn.cursor()
            self._init_db()
        else:
            self.file_name = 'todo.txt'
            self._load_tasks()
    
    def _init_db(self):
        """Initialize the database table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                created_at TEXT,
                completed INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from the storage"""
        self.tasks = []
        
        if self.storage_type == 'db':
            self.cursor.execute('SELECT id, task, created_at, completed FROM tasks ORDER BY created_at')
            rows = self.cursor.fetchall()
            for row in rows:
                self.tasks.append({
                    'id': row[0],
                    'task': row[1],
                    'created_at': row[2],
                    'completed': bool(row[3])
                })
        else:
            if os.path.exists(self.file_name):
                with open(self.file_name, 'r') as file:
                    for line in file:
                        if line.strip():
                            parts = line.strip().split('|')
                            self.tasks.append({
                                'id': int(parts[0]),
                                'task': parts[1],
                                'created_at': parts[2],
                                'completed': parts[3] == 'True'
                            })
    
    def add_task(self, task):
        """Add a new task to the list"""
        task_id = len(self.tasks) + 1
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_task = {
            'id': task_id,
            'task': task,
            'created_at': created_at,
            'completed': False
        }
        
        if self.storage_type == 'db':
            self.cursor.execute(
                'INSERT INTO tasks (task, created_at, completed) VALUES (?, ?, ?)',
                (task, created_at, 0)
            )
            self.conn.commit()
            new_task['id'] = self.cursor.lastrowid
        else:
            with open(self.file_name, 'a') as file:
                file.write(f"{task_id}|{task}|{created_at}|False\n")
        
        self.tasks.append(new_task)
        print(f"Task added: {task}")
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                
                if self.storage_type == 'db':
                    self.cursor.execute(
                        'UPDATE tasks SET completed = 1 WHERE id = ?',
                        (task_id,)
                    )
                    self.conn.commit()
                else:
                    self._save_all_tasks_to_file()
                
                print(f"Task completed: {task['task']}")
                return
        
        print(f"Task with ID {task_id} not found.")
    
    def delete_task(self, task_id):
        """Delete a task from the list"""
        task_to_delete = None
        for task in self.tasks:
            if task['id'] == task_id:
                task_to_delete = task
                break
        
        if task_to_delete:
            self.tasks.remove(task_to_delete)
            
            if self.storage_type == 'db':
                self.cursor.execute(
                    'DELETE FROM tasks WHERE id = ?',
                    (task_id,)
                )
                self.conn.commit()
            else:
                self._save_all_tasks_to_file()
            
            print(f"Task deleted: {task_to_delete['task']}")
        else:
            print(f"Task with ID {task_id} not found.")
    
    def _save_all_tasks_to_file(self):
        """Save all tasks to the text file (overwrites existing file)"""
        with open(self.file_name, 'w') as file:
            for task in self.tasks:
                file.write(f"{task['id']}|{task['task']}|{task['created_at']}|{task['completed']}\n")
    
    def display_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("No tasks in the list.")
            return
        
        print("\nTo-Do List:")
        print("-" * 40)
        for task in self.tasks:
            status = "✓" if task['completed'] else " "
            print(f"{task['id']}. [{status}] {task['task']} (Added: {task['created_at']})")
        print("-" * 40)
    
    def __del__(self):
        """Clean up when the object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    print("Welcome to the To-Do List App!")
    
    # Let user choose storage type
    while True:
        storage_choice = input("Choose storage type (1 for text file, 2 for SQLite database): ").strip()
        if storage_choice == '1':
            todo = ToDoList('txt')
            break
        elif storage_choice == '2':
            todo = ToDoList('db')
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. Complete task")
        print("3. Delete task")
        print("4. View tasks")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            task = input("Enter the task: ").strip()
            if task:
                todo.add_task(task)
            else:
                print("Task cannot be empty!")
        elif choice == '2':
            todo.display_tasks()
            try:
                task_id = int(input("Enter the task ID to mark as complete: ").strip())
                todo.complete_task(task_id)
            except ValueError:
                print("Please enter a valid task ID.")
        elif choice == '3':
            todo.display_tasks()
            try:
                task_id = int(input("Enter the task ID to delete: ").strip())
                todo.delete_task(task_id)
            except ValueError:
                print("Please enter a valid task ID.")
        elif choice == '4':
            todo.display_tasks()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()