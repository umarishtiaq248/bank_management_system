
from django.urls import path
from django.contrib import admin
from . import  views
from .views import BankView,DeleteAccount,SearchAccount,AccountView,LoginView,Logout

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(),name='logout'),
    path('bank/', BankView.as_view(), name='banks'),
    path('bank/admin/', admin.site.urls),
    path("account/<int:bank_id>/", AccountView.as_view(), name="accounts"),
    path('del_account/<int:pk>/', DeleteAccount.as_view(), name='del_account'),
    path('search_account/', SearchAccount.as_view(), name='search_account'),
]
