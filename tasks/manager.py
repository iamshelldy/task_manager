from datetime import datetime

from tasks import Task, Status, Priority
from tasks.utils import load_data, dump_data


class TaskManager:
    """
    A class for managing tasks, including creating,
    modifying, deleting, and filtering tasks.

    The TaskManager provides functionality for handling tasks
    stored in a file. It allows tasks to be created, modified,
    deleted, and filtered by various attributes such as ID, category,
    status, and keywords. The tasks are loaded from the specified
    file and updated after each operation.

    Attributes:
        _tasks_file (str): Path to the file where tasks are stored.
        _categories (set): A set of categories associated with the tasks.
        _tasks (list[Task]): A list of Task objects that are
                             currently managed by the TaskManager.
        _new_task_id (int): The ID to be assigned to the next created task.

    Notes:
        - Task ID management: New tasks are assigned
        incremental IDs starting from 1.
        - Task file format: Tasks are stored in a JSON file
        with the format specified by the Task class.
        - Error handling: The methods handle invalid inputs (e.g.,
        invalid status, priority) and provide feedback to the user.
    """
    def __init__(self, tasks_file_path: str):
        self._tasks_file = tasks_file_path
        self._categories = set()  # Cache for tasks categories.
        self._tasks = load_data(self._tasks_file, self._categories)

        # Id of a new task. (last task id + 1)
        if len(self._tasks) == 0:
            self._new_task_id = 1
        else:
            self._new_task_id = self._tasks[-1].id + 1

    def get_tasks_by_filters(self, **kwargs) -> list[Task]:
        """
        Retrieves a list of tasks filtered by specified criteria.

        The method allows filtering tasks by category, status, task ID,
        and keywords. It applies all filters provided in the function
        arguments and returns a list of tasks that match all given criteria.

        :param kwargs: A dictionary of filter criteria, which includes:
            category (str): The category of the task.
            status (str): The status of the task.
            id (int): The ID of the task.
            key_words (list of str): A list of keywords to search for in
                                     the title and description of the task

        :return: (list[Task]): A list of tasks that match all of specified filters.
                               If no tasks match, an empty list is returned.

        Notes:
            - The 'category' and 'status' values are case-insensitive.
            - The 'key_words' filter checks if any of the specified keywords appear
                              in the task's title or description (case-insensitive).
            - If no filters are applied, the method returns all tasks.
        """
        if not self._tasks:
            return []

        filters = dict()
        key_words = kwargs.get("key_words", [])

        # Check category, if it's given.
        if "category" in kwargs:
            if kwargs["category"].capitalize() not in self._categories:
                return []  # If category don't cached, return no tasks.
            filters["category"] = kwargs["category"].capitalize()
        # Put status filter, if it's given.
        if "status" in kwargs:
            filters["status"] = kwargs["status"].capitalize()
        # Put id filter, if it's given.
        if "id" in kwargs:
            filters["id"] = kwargs["id"]

        # Add keyword filtering to title and description.
        if key_words:
            filters["key_words"] = key_words

        result = []

        for task in self._tasks:
            if all(getattr(task, key, None) == value for key, value in filters.items()
                   if key != "key_words"):
                # Filtering by keywords in title and description.
                if key_words:
                    title = task.title.lower()
                    description = task.description.lower()

                    # Check if the title or description contains keywords.
                    if not any(keyword.lower() in title or keyword.lower() in
                               description for keyword in key_words):
                        print(key_words)
                        continue

                result.append(task)

        return result

    def get_current_tasks(self) -> list[Task]:
        """
        :return: (list[Task]): A list of tasks that match Status("Не выполнена")
        """
        return self.get_tasks_by_filters(status=Status.in_work)

    def create_task(self, title: str, description: str, category: str,
                    deadline: str, priority: str) -> None:
        """
        The method validates the task's deadline to ensure it's a future
        date. It also validates that the deadline follows the ISO 8601
        format (YYYY-MM-DD). If any of the input values are invalid, no
        task is created, and an error message is shown.

        :param title: The title of the task.
        :param description: The description of the task.
        :param category: The category of the task.
        :param deadline: The deadline of the task.
        :param priority: The priority of the task.

        :return: None

    Notes:
        - The deadline must be in the future; otherwise,
          the task will not be created.
        - The title, description, and category are
          capitalized before being saved.
        - If the task is successfully created, it is added to the
          task list, and the task data is saved to the file.
        """
        try:
            deadline = datetime.fromisoformat(deadline)
            if deadline.date() < datetime.now().date():
                print("Task's deadline must be in the future. No tasks created.")
                return
        except ValueError:
            print("Task's deadline must have ISO 8601 format: YYYY-MM-DD. No tasks created.")
            return

        try:
            task = Task(self._new_task_id, title.capitalize(), description.capitalize(),
                        category.capitalize(), deadline, priority, Status.in_work)
        except ValueError as e:
            print(f"{e}. No tasks created.")
            return

        self._categories.add(task.category)
        self._new_task_id += 1
        self._tasks.append(task)

        print("Task was successfully created.")
        # Update file after task creation.
        dump_data(self._tasks, self._tasks_file)

    def modify_tasks(self, task_id: int, new_title: str = None,
                    new_description: str = None, new_priority: str = None,
                    new_status: str = None) -> None:
        """
        Modifies an existing task with the specified task_id by updating its details.

        The method checks that the task with the given task_id exists and
        validates the new values for priority and status. If the task is found,
        it updates the task attributes (title, description, priority, status)
        with the new values. If any of the new values are invalid, an error
        message is displayed, and no changes are made.

        :param task_id: The ID of the task to modify.
        :param new_title: The new title of the task.
        :param new_description: The new description of the task.
        :param new_priority: The new priority of the task.
        :param new_status: The new status of the task.

        :return: None

        Notes:
            - The task ID must exist, and the new
              priority and status must be valid.
            - If the task is successfully modified,
              the changes are saved to the task file.
            - If any errors occur, no changes will be
              made to the tasks or the file.
        """
        # Check that the ID of the task to be modified is less than
        # or equal to the ID of the last written task. ID of the last
        # written task == self._new_task_id - 1.
        if task_id >= self._new_task_id:
            print("No task found.")
            return

        # Check the task priority if it will change.
        if new_priority:
            try:
                new_priority = Priority(new_priority)
            except ValueError as e:
                print(f"{e}. No tasks modified.")
                return

        # Check the task status if it changes.
        if new_status:
            try:
                new_status = Status(new_status)
            except ValueError as e:
                print(f"{e}. No tasks modified.")
                return

        # Get tasks with the specified task_id. Plural, since
        # there is a possibility that the user will open the
        # json file and corrupt the data manually.
        tasks_to_modify = self.get_tasks_by_filters(id=task_id)

        if len(tasks_to_modify) == 0:
            print("No tasks found.")
            return

        # Apply new values if passed.
        for task in tasks_to_modify:
            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            if new_priority:
                task.priority = new_priority
            if new_status:
                task.status = new_status

        print("Task was successfully modified.")
        # Update file after changing task(s).
        dump_data(self._tasks, self._tasks_file)


    def delete_tasks(self, task_id: int = None, category: str = None) -> None:
        """
        Deletes tasks that match the specified
        filters (task_id and/or category).

        The method filters tasks based on the provided task_id and/or
        category. It removes all tasks that meet the filter criteria
        from the internal task list. If any tasks are deleted, the task
        file is updated to reflect the changes. If no matching tasks are
        found, a message is printed indicating that no tasks were deleted.

        :param task_id: the ID of the task to delete.
        :param category: the category of the tasks to delete.

        :return: None

        Notes:
            - If both task_id and category will be provided, the
            tasks must match both filters to be deleted.
            - If no tasks match the given filters, the method
            will print "No tasks found."
            - After deletion, the tasks file is updated with
            the remaining tasks.
        """
        filters = dict()

        # Form a filter based on the passed parameters.
        if category:
            filters["category"] = category
        if task_id:
            filters["id"] = task_id

        # Get tasks to delete.
        tasks_to_delete = self.get_tasks_by_filters(**filters)

        if tasks_to_delete:
            # Save the number of tasks to delete for the report.
            deleted_count = len(tasks_to_delete)

            # Delete all tasks that match the filter.
            self._tasks = [task for task in self._tasks if task not in tasks_to_delete]

            print(f"{deleted_count} task(s) were deleted successfully.")

            # Update the file after deleting the task.
            dump_data(self._tasks, self._tasks_file)
        else:
            print(f"No tasks found.")
