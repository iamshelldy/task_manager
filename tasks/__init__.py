from datetime import datetime
from enum import Enum


class Priority(str, Enum):
    """
    Enum class representing the priority levels for a task.

    The 'Priority' class defines three possible priority levels for
    tasks: high, medium, and low. Each level is represented by a string.
    """
    high = "Высокий"
    medium = "Средний"
    low = "Низкий"

    @classmethod
    def _missing_(cls, value: str) -> Enum | None:
        """
        This method is called when an invalid value is provided to Enum.
        It attempts to map the value to one of the existing priority
        levels, capitalizing the input value.

        :param value: value to be mapped.

        :return: Enum, if match is found, else None.
        """
        return cls._value2member_map_.get(value.capitalize())


class Status(str, Enum):
    """
    Enum class representing the status levels for a task.

    The 'Status' class defines two possible status levels for
    tasks: done and in work. Each level is represented by a string.
    """
    done = "Выполнена"
    in_work = "Не выполнена"

    @classmethod
    def _missing_(cls, value: str) -> Enum | None:
        """
        This method is called when an invalid value is provided to Enum.
        It attempts to map the value to one of the existing priority
        levels, capitalizing the input value.

        :param value: value to be mapped.

        :return: Enum, if match is found, else None.
        """
        return cls._value2member_map_.get(value.capitalize())


class Task:
    """
    Class representing a task.

    A task contains essential information such as its title, description,
    category, deadline, priority, and status. This class allows you to
    create a task with these attributes and provides methods for handling
    and converting the task data to different formats.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title of the task.
        description (str): Detailed description of the task.
        category (str): Category or type of the task.
        deadline (datetime): Deadline of the task, represented
                             as a datetime object.
        priority (Priority): The priority level of the task,
                             represented as a 'Priority' enum.
        status (Status): The status of the task, represented as
                         a 'Status' enum.

    """
    def __init__(self, id: int, title: str, description: str,
                 category: str, deadline: str | datetime,
                 priority: str | Priority, status: str | Status) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.category = category

        self.deadline = self._parse_deadline(deadline)
        self.priority = self._parse_enum(priority, Priority, "Task's priority")
        self.status = self._parse_enum(status, Status, "Task's status")

    @staticmethod
    def _parse_deadline(deadline: str | datetime) -> datetime:
        """
        Converts a deadline string (in ISO 8601 format) or
        datetime object into a datetime object.

        :param deadline: value to be converted into a datetime object.

        :return: datetime object.

        :raises ValueError: if the deadline cannot be
                            converted to datetime object.
        """
        if isinstance(deadline, datetime):
            return deadline
        try:
            return datetime.fromisoformat(deadline)
        except ValueError:
            raise ValueError("Task's deadline must have ISO 8601 format: YYYY-MM-DD")

    @staticmethod
    def _parse_enum(value: str | Enum, enum_cls: type[Enum], field_description: str) -> Enum:
        """
        Converts a string value to a corresponding
        enum member or raises a ValueError if invalid.

        :param value: value to be converted.
        :param enum_cls: Enum class.
        :param field_description: description of the value's
                                  field for the customer.

        :return: Enum member.

        :raises ValueError: If invalid value is provided.
        """
        if isinstance(value, enum_cls):
            return value
        try:
            return enum_cls(value)
        except ValueError:
            raise ValueError(f"{field_description} must be one of {[_.value for _ in enum_cls]}")


    def __str__(self) -> str:
        """
        :return: string representation of the task with
                 its details in a formatted block.
        """
        return (f"/*\n"
                f" * Title:       {self.title}\n"
                f" * ID:          {self.id}\n"
                f" * Description: {self.description}\n"
                f" * Category:    {self.category}\n"
                f" * Deadline:    {self.deadline.strftime('%d.%m.%Y')}\n"
                f" * Priority:    {self.priority.value}\n"
                f" * Status:      {self.status.value}\n"
                f" */")

    def to_dict(self):
        """
        :return: dictionary representation of the task's attributes.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "deadline": self.deadline.date().isoformat(),
            "priority": self.priority.value,
            "status": self.status.value
        }
