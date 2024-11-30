import json

from tasks import Task


def load_data(file_name: str, categories: set) -> list[Task]:
    """
    Loads task data from a JSON file and creates Task objects.

    :param file_name: The path to the JSON file containing task data.
    :param categories: A set that will be updated with task categories.

    :return: A list of Task objects created from the data in the JSON file.

    Note:
        - If the file is not found, an error message is printed.
          Also, will be returned an empty list.
        - If the JSON is invalid, an error message is printed.
          Also, will be returned an empty list.
        - If an error occurs while creating a Task from the data,
          an error message is printed. Task will be skipped.
    """
    json_data = []  # Initialize with empty list, to prevent errors if file is empty.
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"File {file_name} not found")
    except json.decoder.JSONDecodeError:
        print(f"File {file_name} contains invalid JSON")
    except Exception as e:
        print(e)

    result = []
    for task_data in json_data:
        try:
            result.append(Task(**task_data))
            categories.add(task_data["category"])
        except Exception as e:
            print(f"Error while creating Task from data {task_data}: {e}")

    return result


def serialize_task(task_to_serialize: Task) -> dict:
    """
    Serializes a Task object into a dictionary.

    :param task_to_serialize: The Task object to be serialized.

    :return: A dictionary representing the task's attributes.

    :raise TypeError: If the input is not a Task instance.
    """
    if isinstance(task_to_serialize, Task):
        return task_to_serialize.to_dict()
    raise TypeError(f"Type {type(task_to_serialize)} not serializable")


def dump_data(tasks: list[Task], file_name: str) -> None:
    """
    Dumps a list of Task objects into a JSON file.

    :param tasks: A list of Task objects to be serialized and saved.
    :param file_name: The name of the JSON file to be created.

    :return: None.

    Note:
        - If an error occurs while writing to the file,
          an error message will be printed.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(tasks, f, default=serialize_task, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error while writing to file {file_name}: {e}")


def print_tasks(tasks: list[Task]) -> None:
    """
    Prints the details of each task in the provided list.

    :param tasks: A list of Task objects to be printed.

    :return: None.

    If no tasks are found, a message indicating so will be printed.
    """
    if len(tasks) == 0:
        print("No tasks found.")
        return

    print("Tasks found:")
    for task in tasks:
        print(f"{task}")
