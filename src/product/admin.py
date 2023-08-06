from django.contrib import admin
from .models import Variant, Product, ProductImage, ProductVariantPrice, ProductVariant


# Register your models here.

class VariantAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class ProductImageAdmin(admin.ModelAdmin):
    pass


class ProductVariantAdmin(admin.ModelAdmin):
    pass


class ProductVariantPriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Variant, VariantAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductVariantPrice, ProductVariantPriceAdmin)
