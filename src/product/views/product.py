import json

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from product.models import Variant, Product, ProductVariantPrice, ProductVariant, ProductImage


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


def SearchView(request):
    if request.method == 'POST':
        args = request.POST
        # title filter
        product_object = Product.objects.filter(title__icontains=args.get("title"))
        if product_object is None:
            product_object = Product.objects.all()

        # date filter
        date = args.get('date')
        print(date)
        try:
            product_object = product_object.filter(Q(created_at__date=date) | Q(updated_at__date=date))
        except:
            pass

        # variant filter
        variant_object = None
        if not args.get('variant') == '--Select A Variant--':
            variant_object = ProductVariant.objects.filter(variant_title=args.get("variant"))
            variant_object = ProductVariantPrice.objects.filter(Q(product_variant_one=variant_object.first()) |
                                                                Q(product_variant_two=variant_object.first()) |
                                                                Q(product_variant_three=variant_object.first()))
        if variant_object is None:
            variant_object = ProductVariantPrice.objects.all()

        # price filter
        try:
            low = float(args.get("price_from"))
        except:
            low = None
        try:
            high = float(args.get("price_to"))
        except:
            high = None
        try:
            price_object = variant_object.filter(price__gte=low, price__lte=high)
            variant_object = price_object
        except:
            pass
        variant_data = product_variant_data()
        return render(request, 'products/list.html', {'search': True,
                                                      'product': product_object,
                                                      'variant': variant_data,
                                                      'productvariantprice': variant_object})


def product_variant_data():
    data = ProductVariant.objects.all()
    formatted_data = []
    grouped_data = {}

    for item in data:
        variant_title = item.variant.title
        if variant_title not in grouped_data:
            grouped_data[variant_title] = set()
        grouped_data[variant_title].add(item.variant_title)

    for variant_title, variant_values in grouped_data.items():
        formatted_data.append({
            "type": variant_title,
            "value": list(variant_values)
        })

    return formatted_data


def createView(request):
    if request.method == 'POST':
        name = request.POST["productName"]
        sku = request.POST["productSKU"]
        description = request.POST["productDescription"]
        image = request.FILES["mediaFile"]
        file_name = default_storage.get_available_name(image.name)
        file_path = default_storage.save(file_name, ContentFile(image.read()))
        file_url = default_storage.url(file_path)
        product_object = Product.objects.create(title=name, sku=sku, description=description)
        product_image_object = ProductImage.objects.create(product=product_object, file_path=file_url)
        return HttpResponseRedirect('/')


def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.COOKIES['csrftoken']})
