from django.views.generic import DeleteView, ListView, DetailView
from django.shortcuts import render,get_object_or_404,redirect
from .models import Bank,Account
from django.urls import reverse_lazy
from django.http import Http404
from .forms import BankForm,AccountForm

class BankView(ListView):
    model = Bank
    template_name = "banks/index.html"
    form_class = BankForm
    context_object_name = "banks"
    success_url = reverse_lazy('banks')
    def get_queryset(self):
        return Bank.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Save the new bank
            form.save()
            return redirect(self.success_url)
        else:
            return self.get(request, *args, **kwargs)

class AccountView(ListView):
    model = Account,Bank
    form_class=AccountForm
    template_name = "banks/accounts.html"
    context_object_name = "all_accounts"
    success_url = reverse_lazy('accounts')

    def get_queryset(self):
        bank_id = self.kwargs['bank_id']
        bank = get_object_or_404(Bank, pk=bank_id)
        return Account.objects.filter(bank=bank)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bank_id = self.kwargs['bank_id']
        bank = get_object_or_404(Bank, pk=bank_id)
        context['bank'] = bank
        context['form'] = self.form_class()  # Add the form to context
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        bank_id = self.kwargs['bank_id']
        bank = get_object_or_404(Bank, pk=bank_id)
        if form.is_valid():
            account=form.save(commit=False)
            account.bank = bank
            account.save()
            return redirect(reverse_lazy('accounts', kwargs={'bank_id': bank_id}))
        else:
            return self.get(request, *args, **kwargs)


class DeleteBank(DeleteView):
    model = Bank
    template_name = "banks/index.html"
    context_object_name = "bank"
    success_url = reverse_lazy('banks')


class DeleteAccount(DeleteView):
    model = Account
    template_name = 'banks/accounts.html'
    context_object_name = 'account'
    success_url = reverse_lazy('accounts')

    def get_success_url(self):
        bank_id = self.object.bank.id
        return reverse_lazy('accounts', kwargs={'bank_id': bank_id})

    def get_object(self, queryset=None):
        account = super().get_object(queryset)
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
            return Account.objects.filter(user_name__iexact=search_query)  # Filter by user_name
        return Account.objects.all()