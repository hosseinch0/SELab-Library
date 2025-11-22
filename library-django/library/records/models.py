from django.db import models
import uuid
from django.contrib.auth.models import User
from book.models import BookModel
from datetime import timedelta
from django.utils import timezone
# Create your models here.


class RecordsModel(models.Model):
    borrow_record_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'record'

    def is_overdue(self):
        if self.return_date:
            return False

        return timezone.now() > self.due_date

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=30)

        is_new = self._state.adding

        if is_new:
            book = self.book_id
            if book.total_copies > 0:
                book.total_copies -= 1
                book.save()
            else:
                raise ValueError("No copies available for borrowing!")

        else:
            if self.is_returned and self.return_date:
                book = self.book_id
                book.total_copies += 1
                book.save()

        super().save(*args, **kwargs)


class FineModel(models.Model):
    fine_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    record_id = models.ForeignKey(RecordsModel, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    issued_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()

    class Meta:
        verbose_name = 'fine'
