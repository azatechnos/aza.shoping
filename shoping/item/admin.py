from django.contrib import admin

# Register your models here.
from item.models import Category, Product, CategoryImage

admin.site.register(CategoryImage)
admin.site.register(Category)
admin.site.register(Product)