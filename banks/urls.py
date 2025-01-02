from django.urls import path
from django.contrib import admin

urlpatterns = [
    path("banks/", admin.site.urls),
]
