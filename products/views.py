from django.shortcuts import render, get_object_or_404, redirect
from .models import Products
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def product_catalog(request):
    products_list = Products.objects.all()
    
    # Get search parameter
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(pro_name__istartswith=search_query)
    
    # Get category filter
    category = request.GET.get('category', '')
    if category:
        products_list = products_list.filter(pro_Therapeutic_Category=category)
    
    # Get product type filter
    product_type = request.GET.get('type', '')
    if product_type:
        products_list = products_list.filter(pro_type=product_type)
    
    # Pagination
    paginator = Paginator(products_list, 9)  # 9 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'search_query': search_query,
        'selected_category': category,
        'selected_type': product_type,
        'therapeutic_categories': Products.THERAPEUTIC_CATEGORIES,
        'product_types': Products.PRODUCT_TYPES,
    }
    return render(request, 'product_catalog2.html', context)

def benicillins(request):
    # Get all products
    products_list = Products.objects.filter(pro_Therapeutic_Category='Antibiotics')
    
    # Pagination
    paginator = Paginator(products_list, 9)  # 9 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
    }
    return render(request, 'benicillins.html', context)

def General(request):
    # Get all products
    products_list = Products.objects.filter(pro_Therapeutic_Category='Antibiotics')
    
    # Pagination
    paginator = Paginator(products_list, 9)  # 9 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
    }
    return render(request, 'General.html', context)


def cephalosporins(request):
    # Get all products
    products_list = Products.objects.filter(pro_Therapeutic_Category='Antibiotics')
    
    # Pagination
    paginator = Paginator(products_list, 9)  # 9 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
    }
    return render(request, 'cephalosporins.html', context)

def product_info(request):
    try:
        # Get the product ID from query parameters and convert to integer
        product_id = int(request.GET.get('id'))
        # Get the specific product by ID using get_object_or_404
        product = get_object_or_404(Products, id=product_id)
        
        # Get the referring page URL
        referer = request.META.get('HTTP_REFERER', '')
        
        # Determine which page to redirect to in case of error
        if 'benicillins' in referer:
            redirect_url = 'benicillins'
        else:
            redirect_url = 'product_catalog'
            
        context = {
            'product': product,
        }
        return render(request, 'product_info.html', context)
    except (ValueError, TypeError):
        # Handle invalid product ID by redirecting to the appropriate page
        if 'benicillins' in request.META.get('HTTP_REFERER', ''):
            return redirect('benicillins')
        return redirect('product_catalog')

def pro_info(request):
    product_id = request.GET.get('id_pro')
    if product_id:
        product = get_object_or_404(Products, id_pro=product_id)
        return render(request, 'pro_info.html', {'product': product})
    return redirect('product_catalog')