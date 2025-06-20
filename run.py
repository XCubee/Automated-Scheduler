import typer
from scheduler import load_tasks, run_scheduler
from rich import print

def main():
    print("[cyan]Loading tasks and starting the scheduler...[/cyan]")
    load_tasks()
    run_scheduler()

if __name__ == "__main__":
    typer.run(main)
