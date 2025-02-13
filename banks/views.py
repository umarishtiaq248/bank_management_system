from django.contrib.redirects.models import Redirect
from django.views.generic import DeleteView, ListView,CreateView,View
from django.shortcuts import get_object_or_404, redirect, render
from .models import Bank,Account
from django.urls import reverse_lazy,reverse
from django.http import Http404,HttpResponseRedirect,HttpResponse
from .forms import BankForm,AccountForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'banks/login.html')
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', reverse('banks'))
                return redirect(next_url)
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid login credentials.")

class Logout(LoginRequiredMixin,LogoutView):
    def get_success_url(self):
        return reverse_lazy('banks')

class BankView(LoginRequiredMixin,CreateView):
    login_url = '/'
    model = Bank
    template_name = "banks/index.html"
    form_class = BankForm
    context_object_name = "banks"
    success_url = reverse_lazy('banks')
    def get_queryset(self):
        queryset = Bank.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['banks'] = self.get_queryset()
        return context

class AccountView(LoginRequiredMixin,CreateView):
    login_url = '/'
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
        context[self.context_object_name] = self.get_queryset()
        context['bank'] = bank
        context['user'] = self.request.user
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        bank_id = self.kwargs['bank_id']
        bank = get_object_or_404(Bank, pk=bank_id)
        if form.is_valid():
            account=form.save(commit=False)
            account.bank = bank
            account.user = request.user
            account.save()
            return redirect(reverse_lazy('accounts', kwargs={'bank_id': bank_id}))
        else:
            return self.get(request, *args, **kwargs)

class DeleteAccount(LoginRequiredMixin,DeleteView):
    login_url = '/'
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


class SearchAccount(LoginRequiredMixin,ListView):
    login_url = '/'
    model = Account
    template_name = 'banks/accounts.html'
    context_object_name = 'all_accounts'
    def get_queryset(self):
        search_query = self.request.GET.get('search', '')  # Get the search query from the GET request
        if search_query:
            return Account.objects.filter(user_name__iexact=search_query)  # Filter by user_name
        return Account.objects.all()