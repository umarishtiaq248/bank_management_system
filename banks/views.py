from django.shortcuts import render

# Create your views here.
def banks(request):
    return render(request,"banks/banks.html")