from tkinter.font import names

from django.urls import path
from django.contrib import admin
from . import  views
from .views import BankView,DeleteBank,DeleteAccount,SearchAccount,AccountView

urlpatterns = [
    path('', BankView.as_view(), name='banks'),
    path('del_bank/<int:pk>/', DeleteBank.as_view(), name='del_bank'),
    path("account/<int:bank_id>/", AccountView.as_view(), name="accounts"),
    path('del_account/<int:pk>/', DeleteAccount.as_view(), name='del_account'),
    path('search_account/', SearchAccount.as_view(), name='search_account'),
]
