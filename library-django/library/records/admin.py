from django.contrib import admin
from .models import FineModel, RecordsModel
# Register your models here.


class FineAdminModel(admin.ModelAdmin):
    list_display = ['record_id', 'paid', 'issued_date']
    list_filter = ['paid']
    readonly_fields = ['fine_id', 'amount', 'record_id', 'issued_date']


class RecordsAdminModel(admin.ModelAdmin):
    list_display = ['user_id', 'is_returned', 'due_date', 'return_date']
    list_filter = ['user_id', 'is_returned']
    readonly_fields = ['borrow_record_id', ]


admin.site.register(FineModel, FineAdminModel)
admin.site.register(RecordsModel, RecordsAdminModel)
