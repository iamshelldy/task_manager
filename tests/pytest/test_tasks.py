import pytest
from datetime import datetime
from tasks import Task, Priority, Status


@pytest.fixture
def valid_task_data():
    return {
        "id": 1,
        "title": "Test Task",
        "description": "A sample task for testing.",
        "category": "Work",
        "deadline": "2025-12-31",
        "priority": "Высокий",
        "status": "Выполнена"
    }


# Tests for Task creation
def test_create_task_with_valid_data(valid_task_data):
    task = Task(**valid_task_data)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.deadline == datetime(2025, 12, 31)
    assert task.priority == Priority.high
    assert task.status == Status.done


def test_create_task_with_datetime_deadline(valid_task_data):
    valid_task_data["deadline"] = "2027-11-21"
    task = Task(**valid_task_data)
    assert task.deadline.year == 2027
    assert task.deadline.month == 11
    assert task.deadline.day == 21


# Tests for errors handling
def test_invalid_deadline_format(valid_task_data):
    valid_task_data["deadline"] = "31-12-2025"
    with pytest.raises(ValueError, match="Task's deadline must have ISO 8601 format: YYYY-MM-DD"):
        Task(**valid_task_data)


# def test_deadline_in_the_past(valid_task_data):
#     valid_task_data["deadline"] = "2000-01-01"
#     with pytest.raises(ValueError, match="Task's deadline must be in the future"):
#         Task(**valid_task_data)


def test_invalid_priority(valid_task_data):
    valid_task_data["priority"] = "string string"
    with pytest.raises(ValueError, match="Task's priority must be one of .*"):
        Task(**valid_task_data)


def test_invalid_status(valid_task_data):
    valid_task_data["status"] = "string"
    with pytest.raises(ValueError, match="Task's status must be one of .*"):
        Task(**valid_task_data)


# Tests for other methods
def test_to_dict(valid_task_data):
    task = Task(**valid_task_data)
    result = task.to_dict()
    assert result == {
        "id": 1,
        "title": "Test Task",
        "description": "A sample task for testing.",
        "category": "Work",
        "deadline": "2025-12-31",
        "priority": "Высокий",
        "status": "Выполнена"
    }


def test_str_representation(valid_task_data):
    task = Task(**valid_task_data)
    task_str = str(task)
    assert "Title:       Test Task" in task_str
    assert "Deadline:    31.12.2025" in task_str
    assert "Priority:    Высокий" in task_str
    assert "Status:      Выполнена" in task_str
