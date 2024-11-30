from pathlib import Path
import argparse

from tasks.utils import print_tasks
from tasks.manager import TaskManager


TASKS_FILE = str(Path(__file__).parent / "data.json")


def run_cli(args, manager: TaskManager) -> None:
    """
    Processes CLI commands and executes the corresponding TaskManager actions.

    :param args: Parsed command-line arguments from the argparse parser.
    :param manager: An instance of TaskManager to handle tasks.

    Note:
        This function relies on TaskManager methods for error handling.
        If the command or arguments are invalid, appropriate error
        messages are displayed.
    """
    match args.command:
        case "create":
            manager.create_task(
                title=args.title,
                description=args.description,
                category=args.category,
                deadline=args.deadline,
                priority=args.priority
            )
        case "delete":
            manager.delete_tasks(
                task_id=args.id,
                category=args.category
            )
        case "find":
            if args.keywords:
                args.keywords = args.keywords.split(" ")

            filters = {
                "category": args.category,
                "key_words": args.keywords,
                "status": args.status
            }
            # Remove keys with None values.
            filters = {key: value for key, value in filters.items() if value is not None}

            tasks = manager.get_tasks_by_filters(**filters)
            print_tasks(tasks)
        case "list":
            print_tasks(manager.get_current_tasks())
        case "modify":
            content_to_modify = {
                "new_title": args.title,
                "new_description": args.description,
                "new_priority": args.priority,
                "new_status": args.status
            }
            # Remove keys with None values.
            content_to_modify = {
                key: value for key, value in content_to_modify.items() if value is not None
            }

            manager.modify_tasks(
                task_id=args.id,
                **content_to_modify
            )


def main() -> None:
    """
    Entry point of the Task Manager application.

    Parses command-line arguments, initializes the TaskManager,
    and dispatches CLI commands to the appropriate functionality.

    Supported commands:
        - create: Adds a new task with provided details.
        - delete: Deletes tasks by ID or category.
        - find: Searches for tasks based on filters like category, ID, or keywords.
        - list: Lists all tasks with status 'Не выполнена'.
        - modify: Updates the details of an existing task.

    The TaskManager instance uses a file-based system to load and persist tasks.
    """
    parser = argparse.ArgumentParser(
        description="Task Manager designed to manage tasks effectively.",
    )

    subparsers = parser.add_subparsers(dest="command")

    parser_create = subparsers.add_parser(
        "create", help="create task"
    )
    parser_create.add_argument("title", help="task name")
    parser_create.add_argument("description", help="task description")
    parser_create.add_argument("category", help="task category")
    parser_create.add_argument("deadline",
                               help="deadline in ISO format YYYY-MM-DD")
    parser_create.add_argument("priority", help="task priority")

    parser_delete = subparsers.add_parser(
        "delete", help="delete task"
    )
    parser_delete.add_argument("-i", "--id", type=int,
                               help="id of the task to delete")
    parser_delete.add_argument("-c", "--category",
                               help="category of the task to delete")

    parser_find = subparsers.add_parser(
        "find", help="find tasks by filters"
    )
    parser_find.add_argument("-c", "--category", help="tasks category to find")
    parser_find.add_argument("-kw", "--keywords", help="tasks key words to find")
    parser_find.add_argument("-s", "--status", help="tasks status to find")

    parser_list = subparsers.add_parser(
        "list", help="show all current tasks"
    )

    parser_modify = subparsers.add_parser(
        "modify", help="modify task"
    )
    parser_modify.add_argument("id", type=int, help="id of the task to modify")
    parser_modify.add_argument("-t", "--title", help="new title")
    parser_modify.add_argument("-d", "--description", help="new description")
    parser_modify.add_argument("-p", "--priority", help="new priority")
    parser_modify.add_argument("-s", "--status", help="new status")

    args = parser.parse_args()
    manager = TaskManager(TASKS_FILE)

    if any(vars(args).values()):
        # If arguments given, run CLI.
        run_cli(args, manager)
    else:
        # If no arguments, print help.
        parser.print_help()


if __name__ == "__main__":
    main()
