from logging import exception

from django.shortcuts import render,get_object_or_404,redirect
from .models import Bank,Account
from django.contrib import messages


def bank(request):
    try:
        if request.method == "POST":
            bank_name = request.POST.get("bank_name")
            branch_name = request.POST.get("branch_name")
            is_islamic=request.POST.get("is_islamic")
            bank = Bank(bank_name=bank_name, branch_name=branch_name, is_islamic=is_islamic)
            bank.save()
            messages.success(request, 'Bank added successfully!')
            return redirect('banks')
    except:
        pass
    banks = Bank.objects.all()
    return render(request, "banks/index.html",{"banks": banks})


def account(request,bank_id=None):
    bank = get_object_or_404(Bank,pk=bank_id)  # Fetch the bank based on the bank_id passed in the URL
    try:
        if request.method=="POST":
            user_name=request.POST.get("user_name")
            balance=request.POST.get("balance")
            account_obj=Account(user_name=user_name,balance=balance,bank=bank)
            account_obj.save()
            messages.success(request, 'Bank added successfully!')
            return redirect('accounts')
    except:
        pass
    all_account=Account.objects.all()
    return render(request, "banks/accounts.html",{"all_accounts":all_account })