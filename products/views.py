from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Products
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def product_catalog(request):
    lang = request.LANGUAGE_CODE
    products_list = Products.objects.all()

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(pro_name_en__istartswith=search_query)

    # Filters
    category = request.GET.get('category', '')
    if category:
        products_list = products_list.filter(pro_Therapeutic_Category=category)

    product_type = request.GET.get('type', '')
    if product_type:
        products_list = products_list.filter(pro_type=product_type)

    # Pagination
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'lang': lang,
        'search_query': search_query,
        'selected_category': category,
        'selected_type': product_type,
        'therapeutic_categories': Products.THERAPEUTIC_CATEGORIES,
        'product_types': Products.PRODUCT_TYPES,
    }
    return render(request, 'product_catalog2.html', context)


def benicillins(request):
    lang = request.LANGUAGE_CODE
    products_list = Products.objects.filter(pro_Therapeutic_Category='Antibiotics')

    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'benicillins.html', {'products': products, 'lang': lang})


def General(request):
    lang = request.LANGUAGE_CODE
    products_list = Products.objects.filter(pro_Therapeutic_Category='Antibiotics')

    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'General.html', {'products': products, 'lang': lang})


def cephalosporins(request):
    lang = request.LANGUAGE_CODE
    products_list = Products.objects.filter(pro_Therapeutic_Category='Antibiotics')

    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'cephalosporins.html', {'products': products, 'lang': lang})


def product_info(request):
    lang = request.LANGUAGE_CODE
    try:
        product_id = int(request.GET.get('id'))
        product = get_object_or_404(Products, id=product_id)
        referer = request.META.get('HTTP_REFERER', '')
        redirect_url = 'benicillins' if 'benicillins' in referer else 'product_catalog'

        return render(request, 'product_info.html', {'product': product, 'lang': lang})
    except (ValueError, TypeError):
        if 'benicillins' in request.META.get('HTTP_REFERER', ''):
            return redirect('benicillins')
        return redirect('product_catalog')


def pro_info(request):
    lang = request.LANGUAGE_CODE
    product_id = request.GET.get('id_pro')
    if product_id:
        product = get_object_or_404(Products, id_pro=product_id)
        product_image = product.pro_photo_ar if lang == 'ar' else product.pro_photo_en
        return render(request, 'pro_info.html', {
            'product': product,
            'product_image': product_image,
            'lang': lang,
        })
    return redirect('product_catalog')



def search_products(request):
    term = request.GET.get('term', '')
    products = Products.objects.filter(pro_name_en__icontains=term)[:10]
    suggestions = list(products.values_list('pro_name_en', flat=True))
    return JsonResponse(suggestions, safe=False)


def product_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        matching_products = Products.objects.filter(pro_name_en__icontains=query).values_list('pro_name_en', flat=True)[:10]
        suggestions = list(matching_products)
    else:
        suggestions = []
    return JsonResponse({'suggestions': suggestions})
