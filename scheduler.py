"""
Scheduler Module
----------------
Handles loading tasks from config.json and scheduling them using the schedule library.

How to add a new task:
1. Create a Python file in the tasks/ directory (see tasks/task_template.py).
2. Implement your function (e.g., def run(): ...).
3. Add an entry to config.json with the module and function name, and the time to run.
"""
import schedule
import time
import importlib
import json
from datetime import datetime
from rich import print
from rich.table import Table
from rich.console import Console

# Store scheduled jobs for pretty printing
scheduled_jobs = []

def schedule_task(task_func, schedule_time, module_name, function_name):
    """
    Schedule a task based on the time format.
    - 'HH:MM' (e.g., '14:30') for daily at a specific time
    - '*/N' (e.g., '*/10') for every N minutes
    """
    if schedule_time.startswith('*/'):
        minutes = int(schedule_time[2:])
        job = schedule.every(minutes).minutes.do(run_task, task_func=task_func)
        schedule_type = f"Every {minutes} min"
    else:
        job = schedule.every().day.at(schedule_time).do(run_task, task_func=task_func)
        schedule_type = f"Daily at {schedule_time}"
    # Save for pretty printing
    scheduled_jobs.append({
        "Task": module_name,
        "Function": function_name,
        "Schedule": schedule_type
    })
    return job

def load_tasks(config_path="config.json"):
    """
    Load and schedule tasks from the config file.
    Each task should specify:
      - module: Python file in tasks/ (without .py)
      - function: function to call
      - time: when to run (see schedule_task)
    """
    try:
        with open(config_path) as f:
            config = json.load(f)
    except Exception as e:
        print(f"[red]Error loading config file:[/red] {e}")
        return False

    for task in config["tasks"]:
        module_name = task["module"]
        function_name = task["function"]
        schedule_time = task["time"]

        try:
            module = importlib.import_module(f"tasks.{module_name}")
            task_func = getattr(module, function_name)
            print(f"[green]Scheduling:[/green] {module_name}.{function_name} at {schedule_time}")
            schedule_task(task_func, schedule_time, module_name, function_name)
        except Exception as e:
            print(f"[red]Failed to load {module_name}.{function_name}[/red]: {e}")
    return True

def run_task(task_func):
    """Execute a scheduled task with error handling."""
    try:
        print(f"\n[blue]{datetime.now()} - Running task:[/blue] {task_func.__name__}")
        task_func()
    except Exception as e:
        print(f"[red]Error in task {task_func.__name__}: {e}[/red]")

def print_schedule_table():
    console = Console()
    table = Table(title="Current Schedule", show_lines=True)
    table.add_column("Task", style="cyan", no_wrap=True)
    table.add_column("Function", style="magenta")
    table.add_column("Schedule", style="yellow")
    for job in scheduled_jobs:
        table.add_row(job["Task"], job["Function"], job["Schedule"])
    console.print(table)

def run_scheduler():
    """Run the scheduler loop."""
    print("[bold magenta]🚀 Automation Scheduler Started[/bold magenta]")
    print_schedule_table()
    print("\n[cyan]Waiting for scheduled tasks...[/cyan]")
    print("[green] Press Ctrl + C to the end program")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[yellow]Shutting down scheduler...[/yellow]")
            break
        except Exception as e:
            print(f"[red]Scheduler error: {e}[/red]")
            time.sleep(5)     
