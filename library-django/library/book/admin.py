from django.contrib import admin
from .models import BookModel, CategoryModel
# Register your models here.


class BookAdminModel(admin.ModelAdmin):
    list_display = ['title', 'total_copies',
                    'language', 'section', 'row', 'column',]
    list_filter = ['language', 'publisher']
    readonly_fields = ['book_id', 'total_copies',]


class CategoryAdminModel(admin.ModelAdmin):
    list_display = ['name', ]
    readonly_fields = ['category_id']


admin.site.register(BookModel, BookAdminModel)
admin.site.register(CategoryModel, CategoryAdminModel)
