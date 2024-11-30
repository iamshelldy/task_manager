import json
import os

import pytest
from unittest.mock import patch, mock_open

from tasks import Task
from tasks.utils import load_data, serialize_task, dump_data, print_tasks


# Пример данных для теста
valid_task_data = {
    "id": 1,
    "title": "Test Task",
    "description": "This is a test task",
    "category": "Work",
    "deadline": "2027-11-21",
    "priority": "Высокий",
    "status": "Не выполнена"
}

invalid_task_data = {
    "id": 1,
    "title": "Test Task",
    "description": "This is a test task",
    "category": "Work",
    "deadline": "invalid-date",  # Некорректная дата
    "priority": "Высокий",
    "status": "Не выполнена"
}


@pytest.fixture
def file_name():
    return "test_file.json"


# 1. Тесты для load_data
def test_load_data_valid():
    json_data = [valid_task_data]
    with patch("builtins.open", mock_open(read_data=json.dumps(json_data))):
        categories = set()
        tasks = load_data("test_file.json", categories)
        assert len(tasks) == 1
        assert tasks[0].id == 1
        assert tasks[0].title == "Test Task"
        assert "Work" in categories


def test_load_data_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        categories = set()
        tasks = load_data("non_existing_file.json", categories)
        assert tasks == []


def test_load_data_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid-json")):
        categories = set()
        tasks = load_data("test_file.json", categories)
        assert tasks == []


def test_load_data_invalid_task_data():
    json_data = [invalid_task_data]
    with patch("builtins.open", mock_open(read_data=json.dumps(json_data))):
        categories = set()
        tasks = load_data("test_file.json", categories)
        assert len(tasks) == 0
        assert "Work" not in categories


# 2. Тесты для serialize_task
def test_serialize_task():
    task = Task(**valid_task_data)
    serialized = serialize_task(task)
    assert isinstance(serialized, dict)
    assert serialized["id"] == 1
    assert serialized["title"] == "Test Task"


def test_serialize_task_invalid_type():
    with pytest.raises(TypeError):
        serialize_task("invalid-type")


# 3. Тесты для dump_data

@pytest.fixture
def file_name():
    return "test_file.json"


def test_dump_data(file_name):
    task = Task(**valid_task_data)

    # Используем dump_data для записи в файл
    dump_data([task], file_name)

    # Проверяем, что файл существует
    assert os.path.exists(file_name)

    # Открываем файл и читаем его содержимое
    with open(file_name, "r", encoding="utf-8") as f:
        written_data = f.read()

    # Сериализуем данные, как это делается в dump_data
    expected_data = json.dumps([task.to_dict()], ensure_ascii=False, indent=2)

    # Проверяем, что записанные данные совпадают с ожидаемыми
    assert written_data.strip() == expected_data.strip()  # Сравниваем без лишних пробелов

    # Загружаем данные из файла и проверяем, что задача была записана
    categories = set()
    loaded = load_data(file_name, categories)
    assert len(loaded) == 1  # Ожидаем, что загружена одна задача
    assert categories == {"Work"}  # Проверяем, что категория добавлена

    # Удаляем файл после теста
    os.remove(file_name)

# 4. Тесты для print_tasks
@patch("builtins.print")
def test_print_tasks_empty(mock_print):
    print_tasks([])
    mock_print.assert_called_once_with("No tasks found.")


@patch("builtins.print")
def test_print_tasks_with_tasks(mock_print):
    task = Task(**valid_task_data)
    print_tasks([task])
    mock_print.assert_any_call("Tasks found:")
    mock_print.assert_any_call(f"/*\n"
                               f" * Title:       Test Task\n"
                               f" * ID:          1\n"
                               f" * Description: This is a test task\n"
                               f" * Category:    Work\n"
                               f" * Deadline:    21.11.2027\n"
                               f" * Priority:    Высокий\n"
                               f" * Status:      Не выполнена\n"
                               f" */")


