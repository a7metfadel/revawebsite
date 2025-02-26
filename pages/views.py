from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'car-finder-about.html')

def contact(request):
    return render(request, 'contact.html')

def job(request):
    return render(request, 'catalog.html')


def report(request):
    return render(request, 'report.html')

def product_info(request):
    return render(request, 'product_info.html')

def labaratory(request):
    return render(request, 'labaratory.html')

def General(request):
    return render(request, 'General.html')

def cephalosporins(request):
    return render(request, 'cephalosporins.html')

def benicillins(request):
    return render(request, 'benicillins.html')
 