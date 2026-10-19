import threading
from unittest.mock import patch

from django.db import transaction
from django.dispatch import Signal
from django.test import TestCase

from .models import DemoRecord


class SignalBehaviorTests(TestCase):
    def test_synchronous_receiver_finishes_before_send_returns(self):
        signal = Signal()
        events = []

        def receiver(sender, **kwargs):
            events.append("receiver")

        signal.connect(receiver, weak=False)
        events.append("before")
        signal.send(sender=self.__class__)
        events.append("after")

        self.assertEqual(events, ["before", "receiver", "after"])

    def test_receiver_runs_in_calling_thread(self):
        signal = Signal()
        thread_ids = []

        def receiver(sender, **kwargs):
            thread_ids.append(threading.get_ident())

        signal.connect(receiver, weak=False)
        caller_thread_id = threading.get_ident()
        signal.send(sender=self.__class__)

        self.assertEqual(thread_ids, [caller_thread_id])

    def test_created_record_is_rolled_back_with_callers_transaction(self):
        with patch("builtins.print"):
            try:
                with transaction.atomic():
                    DemoRecord.objects.create(name="rollback-example")
                    raise RuntimeError("force rollback")
            except RuntimeError:
                pass

        self.assertFalse(DemoRecord.objects.filter(name="rollback-example").exists())
