# Cubic Engine

A simple, extensible Python automation . Easily add your own tasks and schedule them with a few lines of code.

## Features
- Schedule any Python function to run at specific times or intervals
- Add new tasks by simply creating a Python file in the `tasks/` directory
- Configure all tasks in `config.json`
- See logs and output in your terminal

## Getting Started

### 1. Install Requirements
```
pip install -r requirements.txt
```

### 2. Add Your Task
- Copy `tasks/task_template.py` to a new file in the `tasks/` directory (e.g., `my_task.py`).
- Implement your logic in the `run` function (or any function you want).

Example (`tasks/my_task.py`):
```python
from datetime import datetime

def run():
    print(f"[{datetime.now()}] My custom task is running!")
```

### 3. Configure the Task
- Open `config.json`.
- Add an entry for your task:
```json
{
  "module": "my_task",
  "function": "run",
  "time": "14:30"  // or "*/10" for every 10 minutes
}
```
- `module`: The filename in `tasks/` (without `.py`)
- `function`: The function to call
- `time`: When to run ("HH:MM" for daily, "*/N" for every N minutes)

### 4. Run the engine
```
python run.py
```

## Example config.json
```json
{
  "tasks": [
    {
      "module": "hello_task",
      "function": "say_hello",
      "time": "09:00"
    },
    {
      "module": "my_task",
      "function": "run",
      "time": "*/15"
    }
  ]
}
```

## Tips
- You can add as many tasks as you want.
- All output will appear in your terminal.
- To test, set the time a minute or two ahead and watch the output.

---
