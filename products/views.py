from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Products
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
CATEGORY_TRANSLATIONS = {
    "Analgesic Antipyretic and Muscle-Relaxants": "مسكنات وخافضات حرارة ومرخيات عضلية",
    "Antibiotics": "المضادات الحيوية",
    "Anti Cold and Cough": "مضادات الزكام والسعال",
    "Antifungal": "مضادات الفطور",
    "Antifungal Antiprotozoal": "مضادات الفطور والطفيليات",
    "Bronchodilator": "موسعات الشعب الهوائية",
    "Corticosteroids": "الكورتيكوستيرويدات",
    "Vitamin Supplement": "مكملات الفيتامينات",
    "Nonsteroidal anti-inflammatory drugs": "مضادات الالتهاب غير الستيروئيدية",
    "Cardiovascular Drugs": "أدوية القلب والأوعية الدموية",
    "Antihistamines": "مضادات الهيستامين",
    "Antiseptics": "المطهرات",
    "Fluid & Electrolyte replacement": "تعويض السوائل والشوارد",
    "Gynecology and Genitourinary": "أمراض النساء والجهاز البولي التناسلي",
    "Gastrointestinal Drugs": "أدوية الجهاز الهضمي",
    "Hemorrhoids Medication": "أدوية البواسير",
    "Anti-diabetic drugs": "أدوية السكري",
}

THERAPEUTIC_CATEGORY_FULLNAMES = {
    "Analgesic": "Analgesic Antipyretic and Muscle-Relaxants",
    "Antibiotics": "Antibiotics",
    "Anti_Cold": "Anti Cold and Cough",
    "Antifungal": "Antifungal",
    "Antifungal_Antiprotozoal": "Antifungal Antiprotozoal",
    "Bronchodilator": "Bronchodilator",
    "Corticosteroids": "Corticosteroids",
    "Vitamin": "Vitamin Supplement",
    "NSAID": "Nonsteroidal anti-inflammatory drugs",
    "Cardiovascular": "Cardiovascular Drugs",
    "Antihistamines": "Antihistamines",
    "Antiseptics": "Antiseptics",
    "Fluid_Electrolyte": "Fluid & Electrolyte replacement",
    "Gynecology": "Gynecology and Genitourinary",
    "Gastrointestinal": "Gastrointestinal Drugs",
    "Hemorrhoids": "Hemorrhoids Medication",
    "Anti_diabetic": "Anti-diabetic drugs",
}

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

    # استخراج كل التصنيفات (المفتاح) الموجود فعلياً بالقاعدة
    unique_categories = Products.objects.values_list('pro_Therapeutic_Category', flat=True).distinct()
    unique_categories = [cat for cat in unique_categories if cat]

    # تجهيز التصنيفات للعرض حسب اللغة
    if lang == 'ar':
        therapeutic_categories = [
            (cat, CATEGORY_TRANSLATIONS.get(THERAPEUTIC_CATEGORY_FULLNAMES.get(cat, cat), THERAPEUTIC_CATEGORY_FULLNAMES.get(cat, cat)))
            for cat in unique_categories
        ]
        all_categories = "جميع الفئات"
        filter_title = "حسب الفئة العلاجية"
    else:
        therapeutic_categories = [
            (cat, THERAPEUTIC_CATEGORY_FULLNAMES.get(cat, cat))
            for cat in unique_categories
        ]
        all_categories = "All Categories"
        filter_title = "By Therapeutic Category"

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
        'therapeutic_categories': therapeutic_categories,
        'all_categories': all_categories,
        'filter_title': filter_title,
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
