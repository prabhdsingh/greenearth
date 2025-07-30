from django.contrib import admin

from apps.products.models import Product, EcoTag, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(EcoTag)
admin.site.register(Category)