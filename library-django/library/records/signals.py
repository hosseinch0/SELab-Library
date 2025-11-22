from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from .models import RecordsModel, FineModel


@receiver(post_save, sender=RecordsModel)
def create_fine_if_overdue(sender, instance, created, **kwargs):
    if created:
        return

    if instance.return_date and not instance.is_returned:
        instance.is_returned = True

    if instance.return_date and instance.return_date.date() > instance.due_date.date():
        overdue_days = (instance.return_date.date() -
                        instance.due_date.date()).days
        amount = overdue_days * 20000

        if not FineModel.objects.filter(record_id=instance).exists():
            FineModel.objects.create(
                record_id=instance,
                amount=amount,
                paid=False,
                issued_date=timezone.datetime.now()
            )


@receiver(post_save, sender=FineModel)
def handle_user_on_fine(sender, instance, created, **kwargs):
    user = instance.record_id.user_id
    if created:

        user.is_active = False
        user.save()

    if instance.paid:
        user.is_active = True
        user.save()
