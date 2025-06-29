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

PRODUCT_TYPE_TRANSLATIONS = {
    "Oral Suspension": "معلق فموي",
    "Capsule": "كبسول",
    "Tablets": "مضغوطات",
    "Syrup": "شراب",
    "Suppositories": "تحاميل",
    "Oral Drops": "قطرات فموية",
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

PRODUCT_TYPE_FULLNAMES = {
    "Oral Suspension": "Oral Suspension",
    "Capsule": "Capsule",
    "tablets": "Tablets",
    "Syrup": "Syrup",
    "Suppositories": "Suppositories",
    "Oral Drops": "Oral Drops",
}


def product_catalog(request):
    lang = request.LANGUAGE_CODE
    products_list = Products.objects.all()

    # البحث
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(pro_name_en__istartswith=search_query)

    # الفئة العلاجية
    category = request.GET.get('category', '')
    if category:
        products_list = products_list.filter(pro_Therapeutic_Category=category)

    # الشكل الصيدلاني
    product_type = request.GET.get('type', '')
    if product_type:
        products_list = products_list.filter(pro_type=product_type)

    # استخراج الفئات العلاجية الحقيقية فقط
    unique_categories = Products.objects.values_list('pro_Therapeutic_Category', flat=True).distinct()
    unique_categories = [cat for cat in unique_categories if cat]

    # استخراج الأشكال الصيدلانية الحقيقية فقط
    unique_types = Products.objects.values_list('pro_type', flat=True).distinct()
    unique_types = [typ for typ in unique_types if typ]

    # تجهيز أسماء الفئات والأشكال حسب اللغة
    if lang == 'ar':
        therapeutic_categories = [
            (cat, CATEGORY_TRANSLATIONS.get(THERAPEUTIC_CATEGORY_FULLNAMES.get(cat, cat), THERAPEUTIC_CATEGORY_FULLNAMES.get(cat, cat)))
            for cat in unique_categories
        ]
        product_types = [
            (typ, PRODUCT_TYPE_TRANSLATIONS.get(PRODUCT_TYPE_FULLNAMES.get(typ, typ), PRODUCT_TYPE_FULLNAMES.get(typ, typ)))
            for typ in unique_types
        ]
        all_categories = "جميع الفئات"
        all_types = "جميع الأشكال"
        filter_title = "حسب الفئة العلاجية"
        form_filter_title = "حسب الشكل الصيدلاني"
    else:
        therapeutic_categories = [
            (cat, THERAPEUTIC_CATEGORY_FULLNAMES.get(cat, cat))
            for cat in unique_categories
        ]
        product_types = [
            (typ, PRODUCT_TYPE_FULLNAMES.get(typ, typ))
            for typ in unique_types
        ]
        all_categories = "All Categories"
        all_types = "All Forms"
        filter_title = "By Therapeutic Category"
        form_filter_title = "By pharmaceutical form"

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
        'product_types': product_types,
        'all_categories': all_categories,
        'all_types': all_types,
        'filter_title': filter_title,
        'form_filter_title': form_filter_title,
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

        # إحضار النص الإنجليزي الظاهر للفئة العلاجية والشكل الصيدلاني
        therapeutic_category_en = product.get_pro_Therapeutic_Category_display()
        product_type_en = product.get_pro_type_display()

        # الترجمة حسب اللغة
        if lang == 'ar':
            therapeutic_category_display = CATEGORY_TRANSLATIONS.get(therapeutic_category_en, therapeutic_category_en)
            product_type_display = PRODUCT_TYPE_TRANSLATIONS.get(product_type_en, product_type_en)
        else:
            therapeutic_category_display = therapeutic_category_en
            product_type_display = product_type_en

        return render(request, 'pro_info.html', {
            'product': product,
            'product_image': product_image,
            'lang': lang,
            'therapeutic_category_display': therapeutic_category_display,
            'product_type_display': product_type_display,
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
