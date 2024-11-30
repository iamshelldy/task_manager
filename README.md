# Task Manager Application

This is a **Task Manager** console application designed to manage tasks effectively. It allows users to create, delete, modify, and search tasks, with data stored in a file for persistence.

## Features
- **Create Tasks**: Add new tasks with a title, description, category, deadline, and priority.
- **List Tasks**: Display all existing tasks.
- **Search Tasks**: Find tasks by category, ID, keywords, or status.
- **Modify Tasks**: Update the title, description, priority, or status of an existing task.
- **Delete Tasks**: Remove tasks by ID or category.

## Getting Started

### Prerequisites
- Python 3.10 or later.

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/task-manager.git
    cd task-manager
    ```
2. Install dependencies if needed (e.g., for testing):
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1. Run the application:
    ```bash
    python -m task_manager.main
    ```
2. Use the available commands to manage tasks:
    - `create`: Add a new task.
    - `delete`: Remove tasks by ID or category.
    - `find`: Search tasks by filters (e.g., ID, category, status).
    - `list`: Display all tasks.
    - `modify`: Update task properties like title, description, or status.

### CLI Example
```bash
# Create a new task
python -m main create "buy Groceries" "buy milk, eggs, and bread" "shopping" "2025-12-05" "высокий"

# List all tasks
python -m main list

# Find tasks by category
python -m main find --category "Shopping"

# Modify a task
python -m main modify 1 --status "Выполнена"

# Delete tasks by category
python -m main delete --category "Shopping"
```

## Project Structure
```shell
task_manager/
├── tasks/
│   ├── __init__.py        # Task class implementation
│   ├── manager.py         # TaskManager class implementation
│   ├── utils.py           # Helper functions for loading/dumping data
├── main.py                # Entry point for the application
└── README.md              # Documentation
```

## File Storage
Task data is stored in a JSON file (`tasks.json`). Ensure this file exists in the working directory, or it will be created upon the first task operation.
