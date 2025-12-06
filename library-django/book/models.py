from django.db import models
import uuid
# Create your models here.


class CategoryModel(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=75)
    description = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class BookModel(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=125)
    author = models.CharField(max_length=150, blank=True)
    publisher = models.CharField(max_length=125)
    summary = models.TextField(max_length=500)
    cover_image = models.ImageField(upload_to='images/', blank=True)
    language = models.CharField(max_length=65)
    total_copies = models.IntegerField()
    published_year = models.DateTimeField()
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, blank=True)
    section = models.CharField(max_length=75)
    column = models.CharField(max_length=75)
    row = models.CharField(max_length=75)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'book'
