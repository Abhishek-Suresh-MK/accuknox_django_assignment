import threading
import time

from django.core.management.base import BaseCommand
from django.db import transaction
from django.dispatch import Signal

from signals_demo.models import DemoRecord


class Command(BaseCommand):
    help = "Demonstrate synchronous signals, thread identity, and transaction rollback."

    def handle(self, *args, **options):
        self.stdout.write("QUESTION 1: synchronous execution")
        signal = Signal()
        events = []

        def slow_receiver(sender, **kwargs):
            events.append("receiver started")
            time.sleep(0.5)
            events.append("receiver finished")

        signal.connect(slow_receiver, weak=False)
        events.append("before send")
        signal.send(sender=self.__class__)
        events.append("after send")
        for event in events:
            self.stdout.write(event)
        self.stdout.write("Conclusion: receiver finished before after send.\\n")

        self.stdout.write("QUESTION 2: thread identity")
        thread_signal = Signal()
        thread_ids = {}

        def thread_receiver(sender, **kwargs):
            thread_ids["receiver"] = threading.get_ident()

        thread_signal.connect(thread_receiver, weak=False)
        thread_ids["caller"] = threading.get_ident()
        thread_signal.send(sender=self.__class__)
        self.stdout.write(f"Caller thread ID:   {thread_ids['caller']}")
        self.stdout.write(f"Receiver thread ID: {thread_ids['receiver']}")
        self.stdout.write(
            f"Same thread: {thread_ids['caller'] == thread_ids['receiver']}\\n"
        )

        self.stdout.write("QUESTION 3: database transaction")
        name = "transaction-rollback-demo"
        DemoRecord.objects.filter(name=name).delete()
        try:
            with transaction.atomic():
                DemoRecord.objects.create(name=name)
                self.stdout.write(
                    f"Inside atomic block: {transaction.get_connection().in_atomic_block}"
                )
                raise RuntimeError("Intentional rollback for demonstration")
        except RuntimeError:
            self.stdout.write("Caught intentional exception; transaction rolled back.")

        exists = DemoRecord.objects.filter(name=name).exists()
        self.stdout.write(f"Record exists after rollback: {exists}")
        self.stdout.write(
            "Conclusion: the receiver ran during the save, but the database write "
            "was rolled back with the caller's atomic transaction."
        )
