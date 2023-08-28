from django.contrib import admin

from .models import Category, CategoryItem, CategoryItemData

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryItem)
admin.site.register(CategoryItemData)