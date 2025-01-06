from django.shortcuts import render

# Create your views here.
def products(request):
    return render(request, 'products_catalog.html')

def add_products(request):
    return render(request, 'add_product.html')

def cv(request):
    return render(request, 'cv_form.html')