import tkinter as tk
from tkinter import messagebox
import csv
import os

# File to store tasks
TASKS_FILE = 'tasks.csv'

# Check if the file exists. If not, create it
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Status", "Task"])

        
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("To-Do List")
        
        # Entry to add tasks
        self.task_entry = tk.Entry(self, width=50)
        self.task_entry.pack(pady=10)
        
        # Listbox to display tasks
        self.tasks_listbox = tk.Listbox(self, width=50, height=20)
        self.tasks_listbox.pack(pady=10)
        
        # Buttons
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)
        
        self.delete_button = tk.Button(self, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)
        
        self.mark_complete_button = tk.Button(self, text="Mark as Complete", command=self.mark_completed)
        self.mark_complete_button.pack(pady=5)
        
        # Checkbox to show completed tasks
        self.show_completed_var = tk.IntVar()
        self.show_completed_checkbox = tk.Checkbutton(self, text="Show Completed", variable=self.show_completed_var, command=self.load_tasks)
        self.show_completed_checkbox.pack(pady=10)
        
        # Load tasks from the file
        self.load_tasks()
    
    def add_task(self):
        task = self.task_entry.get()
        if task:
            with open(TASKS_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Incomplete', task])
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")
    
    def delete_task(self):
        try:
            selected_task_index = self.tasks_listbox.curselection()[0]
            all_tasks = self.get_all_tasks()
            del all_tasks[selected_task_index]
            self.save_tasks(all_tasks)
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete!")
    
    def mark_completed(self):
        try:
            selected_task_index = self.tasks_listbox.curselection()[0]
            all_tasks = self.get_all_tasks()
            all_tasks[selected_task_index][0] = 'Completed'
            self.save_tasks(all_tasks)
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as completed!")
    
    def load_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        with open(TASKS_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                status, task = row
                if self.show_completed_var.get() or status == 'Incomplete':
                    self.tasks_listbox.insert(tk.END, f"{status}: {task}")
    
    def get_all_tasks(self):
        with open(TASKS_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            return list(reader)
    
    def save_tasks(self, tasks):
        with open(TASKS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Status", "Task"])
            writer.writerows(tasks)


# Create and run the app
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
