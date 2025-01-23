from tkinter.font import names

from django.urls import path
from django.contrib import admin
from . import  views

urlpatterns = [
    path("", views.bank , name="banks"),
    path("account/<int:bank_id>/", views.account, name="accounts"),
]
