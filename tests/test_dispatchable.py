"""Tests for dispatchable.py"""
from __future__ import annotations

import sys
from typing import Final
from unittest.mock import Mock, call, create_autospec, sentinel

import pytest
from django.dispatch import Signal

from dispatchable import Dispatchable


def reciever_func(*args, **kwargs) -> None:
    """Receiver function mockup"""


SOME_SENDER: Final[object] = object()


@pytest.fixture
def signal() -> Signal:
    """Mockup a Signla object"""
    return create_autospec(Signal, instanc=True)


@pytest.mark.parametrize(
    "sender, pass_sender, expected_reciever_method, expected_dispatch_uid",
    [
        pytest.param(
            None,
            True,
            "receive_signal",
            (reciever_func.__name__, reciever_func.__module__),
            id="no sender",
        ),
        pytest.param(
            None,
            False,
            "receive_signal_drop_sender",
            (reciever_func.__name__, reciever_func.__module__),
            id="no sender and no sender arg",
        ),
        pytest.param(
            SOME_SENDER,
            True,
            "receive_signal",
            (reciever_func.__name__, reciever_func.__module__, SOME_SENDER),
            id="sender given",
        ),
        pytest.param(
            SOME_SENDER,
            False,
            "receive_signal_drop_sender",
            (reciever_func.__name__, reciever_func.__module__, SOME_SENDER),
            id="sender given but no sender arg",
        ),
    ],
)
def test_dispatchable_init(
    sender: object,
    pass_sender: bool,
    expected_reciever_method: str,
    expected_dispatch_uid: tuple[object, ...],
    signal: Signal,
) -> None:
    """
    Test that creating a Dispatchable object connects it to the given signal
    while setting a dispatch_id
    """
    disp = Dispatchable(signal, reciever_func, sender=sender, pass_sender=pass_sender)

    reciever_method = getattr(disp, expected_reciever_method)
    assert signal.connect.call_args_list == [
        call(reciever_method, weak=False, dispatch_uid=expected_dispatch_uid)
    ]


@pytest.fixture
def some_kwargs() -> dict:
    """Some kwargs values"""
    return {"foo": "bar", "baz": "bal"}


@pytest.fixture
def disp_instance(signal: Signal) -> Dispatchable:
    """A Dispatchable for tests"""
    return Dispatchable(signal, reciever_func, sender=SOME_SENDER, pass_sender=True)


def test_receive_signal(
    disp_instance: Dispatchable, some_kwargs: dict, monkeypatch: pytest.MonkeyPatch
):
    """
    Test that receive_signal calls global_patchable_reciever_caller and passes
    it the sender and the kwargs. This also ensures that
    global_patchable_reciever_caller can actually be patched
    """
    some_return_value = sentinel.some_return_value
    rec_caller_mock = Mock(return_value=some_return_value)
    monkeypatch.setattr(
        Dispatchable, "global_patchable_reciever_caller", rec_caller_mock
    )

    out = disp_instance.receive_signal(SOME_SENDER, **some_kwargs)

    assert rec_caller_mock.call_args_list == [call(sender=SOME_SENDER, **some_kwargs)]
    assert out == some_return_value


def test_receive_signal_drop_sender(
    disp_instance: Dispatchable, some_kwargs: dict, monkeypatch: pytest.MonkeyPatch
):
    """
    Test that receive_signal_drop_sender calls global_patchable_reciever_caller
    and passes it the kwargs. This also ensures that
    global_patchable_reciever_caller can actually be patched
    """
    some_return_value = sentinel.some_return_value
    rec_caller_mock = Mock(return_value=some_return_value)
    monkeypatch.setattr(
        Dispatchable, "global_patchable_reciever_caller", rec_caller_mock
    )

    out = disp_instance.receive_signal_drop_sender(SOME_SENDER, **some_kwargs)

    assert rec_caller_mock.call_args_list == [call(**some_kwargs)]
    assert out == some_return_value


def test_global_patchable_reciever_caller(
    disp_instance: Dispatchable, some_kwargs: dict, monkeypatch: pytest.MonkeyPatch
):
    """
    Test that global_patchable_reciever_caller, when unpatched called the
    receiver function in a way that allows patching it
    """
    some_return_value = sentinel.some_return_value
    rec_func_mock = Mock(return_value=some_return_value)
    monkeypatch.setattr(
        sys.modules[reciever_func.__module__], reciever_func.__name__, rec_func_mock
    )

    out = disp_instance.global_patchable_reciever_caller(**some_kwargs)

    assert rec_func_mock.call_args_list == [call(**some_kwargs)]
    assert out == some_return_value
