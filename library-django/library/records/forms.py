from django import forms
from .models import RecordsModel, BookModel, FineModel
from django.utils import timezone


class BorrowForm(forms.ModelForm):
    class Meta:
        model = RecordsModel
        fields = ['borrow_record_id', 'book_id',
                  'borrow_date']
        widgets = {
            'book_id': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['book_id'].disabled = True
        self.fields['borrow_record_id'].disabled = True
        self.fields['borrow_date'].initial = timezone.now()
        self.fields['borrow_date'].disabled = True
