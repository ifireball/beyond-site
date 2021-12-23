"""Tests for the huey-specific fixture we have in conftest.py"""
from pathlib import Path
from typing import Callable
from unittest.mock import Mock, call, sentinel

import pytest
from _pytest.fixtures import SubRequest
from huey.api import Huey, MemoryHuey, RedisHuey, SqliteHuey, TaskWrapper


@pytest.fixture
def huey_sqlite_queue(tmp_path: Path) -> Huey:
    """Create Huey sqlite-based queues for tests"""
    return SqliteHuey(filename=str(tmp_path / "huey.sqlite3"))


@pytest.fixture
def huey_sqlite_immediate_queue(tmp_path: Path) -> Huey:
    """Create Huey immediate sqlite-based queues for tests"""
    return SqliteHuey(filename=str(tmp_path / "huey.sqlite3"), immediate=True)


@pytest.fixture
def huey_memory_queue() -> Huey:
    """Create an in-memory Huey queue for tests"""
    return MemoryHuey()


@pytest.fixture
def heuy_redis_queue() -> Huey:
    """Create an Redis-based Huey queue for tests"""
    return RedisHuey()


@pytest.fixture(
    params=[
        "huey_sqlite_queue",
        "huey_sqlite_immediate_queue",
        "huey_memory_queue",
        "heuy_redis_queue",
    ]
)
def huey_queue(request: SubRequest) -> Huey:
    """Create Huey queues for tests"""
    return request.getfixturevalue(request.param)


@pytest.fixture
def huey_task_func() -> Callable:
    """Create a mocked function to serve as a Heuy task"""
    return Mock(
        name="huey_task_func",
        __name__="huey_task_func",
        return_value=sentinel.huey_task_returned_value,
    )


@pytest.fixture
def huey_task(huey_queue: Huey, huey_task_func: Callable) -> TaskWrapper:
    """Create a Huey task calling a mock object"""
    # The following will raise an exception if we make the fixtures somehow block task creation
    return huey_queue.task()(huey_task_func)


def test_can_define_tasks(huey_task: TaskWrapper) -> None:
    """
    Test that we can alwas define Huey tasks even without Huey support being enabled
    """
    # The included fixture causes a queue and a task to be created which should not raise an error
    assert huey_task


def test_cannot_schedule_tasks(huey_task: TaskWrapper) -> None:
    """
    Test that calling tasks is blocked if the test isn't specially marked
    """
    with pytest.raises(RuntimeError):
        huey_task()


@pytest.mark.huey
def test_marked_calls_tasks_immediately(
    huey_task: TaskWrapper, huey_task_func: Mock
) -> None:
    """
    That that calling tasks in a marked test runs them in a memory-based immediate queue
    """
    huey_task()

    assert huey_task_func.call_args_list == [call()]


@pytest.mark.huey
def test_cannot_set_non_immediate(huey_queue):
    """Test that its impossible to force the queue out of immediate mode"""
    assert huey_queue.immediate
    with pytest.raises(RuntimeError):
        huey_queue.immediate = False
