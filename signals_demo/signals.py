from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DemoRecord


@receiver(post_save, sender=DemoRecord)
def record_post_save(sender, instance, created, **kwargs):
    # Used by the transaction demonstration to show the receiver's context.
    print(
        f"post_save receiver ran; in_atomic_block={connection.in_atomic_block}; "
        f"created={created}"
    )
