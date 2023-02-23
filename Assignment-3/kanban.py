import tkinter as tk
from datetime import datetime, timedelta

class KanbanBoard(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.master.title("Kanban Board")

        # Create the three columns with labels
        self.todo_label = tk.Label(self, text="To Do", font=("Helvetica", 16))
        self.todo_label.pack(side=tk.LEFT, padx=10)
        self.todo = tk.Listbox(self, width=30, height=15)
        self.todo.pack(side=tk.LEFT)

        # Create the "In Progress" column
        self.in_progress_label = tk.Label(self, text="In Progress", font=("Helvetica", 16))
        self.in_progress_label.pack(side=tk.LEFT, padx=10)
        self.in_progress = tk.Listbox(self, width=30, height=15)
        self.in_progress.pack(side=tk.LEFT)

        # Create the "Done" column
        self.done_label = tk.Label(self, text="Done", font=("Helvetica", 16))
        self.done_label.pack(side=tk.LEFT, padx=10)
        self.done = tk.Listbox(self, width=30, height=15)
        self.done.pack(side=tk.LEFT)

        # Create a text entry widget and a button for adding tasks
        self.add_task_entry = tk.Entry(self, width=30)
        self.add_task_entry.pack(side=tk.BOTTOM, pady=10)
        self.add_task_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side=tk.BOTTOM)

        # Bind the events for moving tasks between columns
        self.todo.bind("<<ListboxSelect>>", self.move_task_to_in_progress)
        self.in_progress.bind("<<ListboxSelect>>", self.move_task_to_done)
        self.done.bind("<<ListboxSelect>>", self.delete_task)

        # Create labels for analytics
        self.cycle_time_label = tk.Label(self, text="Cycle Time: N/A")
        self.cycle_time_label.pack(side=tk.BOTTOM, pady=5)
        self.throughput_label = tk.Label(self, text="Throughput: N/A")
        self.throughput_label.pack(side=tk.BOTTOM)

        # Create variables for tracking analytics
        self.tasks_started = {}
        self.tasks_completed = {}

    def add_task(self):
        task = self.add_task_entry.get()
        if task:
            self.todo.insert(tk.END, task)
            self.add_task_entry.delete(0, tk.END)
            self.tasks_started[task] = datetime.now()

    def move_task_to_in_progress(self, event):
        widget = event.widget
        task = widget.get(widget.curselection())
        widget.delete(widget.curselection())
        self.in_progress.insert(tk.END, task)

    def move_task_to_done(self, event):
        widget = event.widget
        task = widget.get(widget.curselection())
        widget.delete(widget.curselection())
        self.done.insert(tk.END, task)
        self.tasks_completed[task] = datetime.now()
        self.update_analytics()

    def delete_task(self, event):
        widget = event.widget
        task = widget.delete(widget.curselection())
        self.tasks_completed[task] = datetime.now()
        self.update_analytics()

    def update_analytics(self):
        completed_tasks = len(self.tasks_completed)
        self.throughput_label.config(text=f"Throughput: {completed_tasks}")
        self.cycle_time_label.config(text=f"Cycle Time: {completed_tasks} seconds")

if __name__ == "__main__":
    root = tk.Tk()
    kb = KanbanBoard(root)
    kb.pack(fill=tk.BOTH, expand=True)
    root.mainloop()



     



