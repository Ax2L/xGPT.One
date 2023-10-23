from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console

console = Console()

todos = ["Buy milk", "Go to gym", "Write code", "Read a book"]
completed = []

def display_todos():
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("No.", style="dim", width=5)
    table.add_column("Task")
    table.add_column("Status")

    for index, todo in enumerate(todos, 1):
        status = "Done" if todo in completed else "Pending"
        table.add_row(str(index), todo, status)

    console.print(table)

def add_todo():
    task = Prompt.ask("Enter new task", default="New Task")
    todos.append(task)

def complete_todo():
    display_todos()
    task_num = IntPrompt.ask("Enter task No. to mark as done", default=0)
    if 0 < task_num <= len(todos):
        completed.append(todos[task_num - 1])
    else:
        console.print("[bold red]Invalid task number![/bold red]")

def main():
    while True:
        console.clear()
        console.print(Panel("[bold]To-Do List[/bold]", expand=False))
        display_todos()
        console.print("\nOptions:\n[1] Add new task\n[2] Complete task\n[3] Exit")
        choice = IntPrompt.ask("Choose an option", choices=[1, 2, 3], default=1)
        
        if choice == 1:
            add_todo()
        elif choice == 2:
            complete_todo()
        elif choice == 3:
            if Confirm.ask("Do you want to exit?"):
                console.print("[bold green]Goodbye![/bold green]")
                break
        else:
            console.print("[bold red]Invalid option![/bold red]")

if __name__ == "__main__":
    main()
