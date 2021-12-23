"""Fixtures that affect everything

This includes things like disabling major IO-causing systems like Huey during tests
"""
import pytest
from _pytest.fixtures import SubRequest
from huey.api import Huey
from huey.storage import BaseStorage, EmptyData


def _raise_huey_blocked_error(*args, **kwargs) -> None:
    raise RuntimeError('Huey access not allowed, use the "huey" mark to enable it')


class BlockedHueyStorage(BaseStorage):
    """
    A Huey storage backend that blocks any writing attempts
    """

    def __init__(self, *args, **kwargs) -> None:
        """Accept any arguments so we can use the class as a makeshift
        `create_storage` method for Huey"""
        super().__init__()

    def enqueue(self, data, priority=None):
        _raise_huey_blocked_error()

    def dequeue(self):
        _raise_huey_blocked_error()

    def queue_size(self):
        return 0

    def enqueued_items(self, limit=None):
        return []

    def flush_queue(self):
        _raise_huey_blocked_error()

    def add_to_schedule(self, data, ts, utc):
        _raise_huey_blocked_error()

    def read_schedule(self, ts):
        return []

    def schedule_size(self):
        return 0

    def scheduled_items(self, limit=None):
        return []

    def flush_schedule(self):
        _raise_huey_blocked_error()

    def put_data(self, key, value, is_result=False):
        _raise_huey_blocked_error()

    def peek_data(self, key):
        return EmptyData

    def pop_data(self, key):
        return EmptyData

    def has_data_for_key(self, key):
        return False

    def result_store_size(self):
        return 0

    def result_items(self):
        return {}

    def flush_results(self):
        _raise_huey_blocked_error()


def _force_in_memory_immediate_storage(self: Huey) -> BaseStorage:
    self.immediate_use_memory = True
    self._immediate = True  # pylint: disable=protected-access
    return self.get_immediate_storage()


def _blocking_immediate_setter(_: Huey, value: bool) -> None:
    if not value:
        raise RuntimeError(
            "Attempt made to bring a Huey queue out of immediate mode. This is"
            "incompatible with testing and was therfore blocked"
        )


@pytest.fixture(autouse=True)
def block_huey(request: SubRequest, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    If test is marked with "huey":
        Force all Huey queues to run in immediate in-memory mode
    Else:
        Block all Huey instances from writing to the storga backend thereby
        preventing them from schedualing tasks
    """
    marker = request.node.get_closest_marker("huey")
    if marker is None:
        monkeypatch.setattr(Huey, "create_storage", BlockedHueyStorage)
        monkeypatch.setattr(Huey, "execute", _raise_huey_blocked_error)
    else:
        monkeypatch.setattr(Huey, "create_storage", _force_in_memory_immediate_storage)
        immediate_prop = property(lambda _: True)
        # Pylint seems to not properly know the type of the `setter` method
        # pylint: disable=assignment-from-no-return,too-many-function-args
        immediate_prop = immediate_prop.setter(_blocking_immediate_setter)
        monkeypatch.setattr(Huey, "immediate", immediate_prop)


def pytest_configure(config):
    """Configure custom stuff for PyTest"""
    config.addinivalue_line(
        "markers", "huey: allow the test to use the Huey task queue"
    )
