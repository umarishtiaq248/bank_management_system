from django import forms
from .models import Bank,Account
class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['bank_name', 'branch_name', 'is_islamic']
        widgets = {
            'is_islamic': forms.RadioSelect(choices=[(True, 'Islamic'), (False, 'Non-Islamic')]),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['user_name', 'balance']