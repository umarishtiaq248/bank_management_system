from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bank(models.Model):
    bank_name=models.CharField(max_length=10)
    branch_name = models.CharField(max_length=10)
    is_islamic = models.BooleanField(null=True)

    def __str__(self):
        return self.bank_name

class Account(models.Model):
    user_id = User.objects.get(username='umar-ishtiaq')
    user_name=models.CharField(max_length=10)
    balance = models.FloatField()
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE,related_name="accounts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts", default=user_id.id)

    def __str__(self):
        return f"{self.user_name}"