from logging import exception
from django.views.generic import View, DeleteView, ListView
from django.shortcuts import render,get_object_or_404,redirect
from .models import Bank,Account
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib import messages

class BankView(View):
    template_name = "banks/index.html"

    def get(self, request):
        banks = Bank.objects.all()  # Fetch all the banks
        context = {
            'banks': banks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        bank_name = request.POST.get('bank_name')
        branch_name = request.POST.get('branch_name')
        is_islamic = request.POST.get('is_islamic')
        if bank_name and branch_name and is_islamic is not None:
            bank = Bank(bank_name=bank_name, branch_name=branch_name, is_islamic=is_islamic == 'True')
            bank.save()
        return redirect('banks')
class AccountView(View):
    template_name = "banks/accounts.html"
    def get(self, request, bank_id):
        bank = get_object_or_404(Bank, pk=bank_id)
        all_accounts = Account.objects.filter(bank_id=bank_id)
        return render(request, self.template_name, {
            'all_accounts': all_accounts,
            'bank':bank
        })
    def post(self, request ,bank_id):
        bank = get_object_or_404(Bank, pk=bank_id)
        user_name = request.POST.get("user_name")
        balance = request.POST.get("balance")
        if user_name and balance:
            account_obj = Account(user_name=user_name, balance=balance, bank=bank)
            account_obj.save()
        return redirect('accounts', bank_id=bank.id)

class DeleteBank(DeleteView):
    model = Bank
    template_name = "banks/index.html"
    context_object_name = "bank"
    success_url = reverse_lazy('banks')


class DeleteAccount(DeleteView):
    model = Account
    template_name = 'banks/accounts.html'
    context_object_name = 'account'

    def get_success_url(self):
        bank_id = self.object.bank.id
        return reverse_lazy('accounts', kwargs={'bank_id': bank_id})

    def get_object(self, queryset=None):
        account = super().get_object(queryset)
        print(account)
        if account is None:
            raise Http404("Account not found")
        return account
class SearchAccount(ListView):
    model = Account
    template_name = 'banks/accounts.html'
    context_object_name = 'all_accounts'
    def get_queryset(self):
        search_query = self.request.GET.get('search', '')  # Get the search query from the GET request
        if search_query:
            return Account.objects.filter(user_name__icontains=search_query)  # Filter by user_name
        return Account.objects.all()