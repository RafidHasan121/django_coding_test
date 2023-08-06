from django.urls import path
from django.views.generic import TemplateView
from .models import Product, ProductVariantPrice, ProductVariant
from product.views.product import CreateProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView

from .views.product import SearchView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
        'search': False,
        'product': Product.objects.all(),
        'productvariantprice': ProductVariantPrice.objects.all(),
        'variant': ProductVariant.objects.all()
    }), name='list.product'),
    path('search/', SearchView)
]
