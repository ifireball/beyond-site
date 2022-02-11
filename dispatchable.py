"""Making `django.dispatch` more test-frindly"""
from __future__ import annotations

import sys
from typing import Callable

from django.dispatch import Signal


class Dispatchable:
    """Object that goes between django.dispatch.Signal objects and the
    callables that need to be connected to them and order to allow for signal
    blocking and receiver monkey patching

    Dispatchable is implemented as a class as opposed to a set of "partial"
    calls in order to allow for global monkey-patching of the class
    """

    _receiver_name: str
    _receiver_module: str

    def __init__(
        self, signal: Signal, receiver: Callable, sender: object, pass_sender: bool
    ) -> None:
        if sender is None:
            dispatch_uid: tuple = (receiver.__name__, receiver.__module__)
        else:
            dispatch_uid = (receiver.__name__, receiver.__module__, sender)
        if pass_sender:
            reciever_method: Callable = self.receive_signal
        else:
            reciever_method = self.receive_signal_drop_sender
        signal.connect(reciever_method, weak=False, dispatch_uid=dispatch_uid)
        self._receiver_name = receiver.__name__
        self._receiver_module = receiver.__module__

    def receive_signal(self, sender: object, **kwargs: object) -> object:
        """This method is attached as the receiver to the Signal objects when
        we want the sender object to be passed along the the receiver
        function"""
        return self.global_patchable_reciever_caller(sender=sender, **kwargs)

    def receive_signal_drop_sender(self, _: object, **kwargs: object) -> object:
        """This method is attached as the receiver to the Signal objects when
        we don't want the sender object to be passed along the the receiver
        function"""
        return self.global_patchable_reciever_caller(**kwargs)

    def global_patchable_reciever_caller(self, **kwargs) -> object:
        """This method does the actual job of calling the receiver function via
        its name and module.  Test systems that want to completely block calls
        to recievers can monky patch it at the class level to do something
        else"""
        module = sys.modules[self._receiver_module]
        receiver = getattr(module, self._receiver_name)
        return receiver(**kwargs)
