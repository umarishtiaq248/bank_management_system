from django import forms
from .models import Bank

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['bank_name', 'branch_name', 'is_islamic']  # Specify the fields to include in the form
        widgets = {
            'is_islamic': forms.RadioSelect(),  # You can customize how the `is_islamic` field is rendered
        }