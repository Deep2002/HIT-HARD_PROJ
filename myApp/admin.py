from django.contrib import admin

from .models import Tag, Product, Cart, Month, Product_Cart

# Register your models here.
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Month)
admin.site.register(Product_Cart)
