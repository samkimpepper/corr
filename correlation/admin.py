from django.contrib import admin

from .models import Account, Category, CategoryItem, CategoryItemData

# Register your models here.
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(CategoryItem)
admin.site.register(CategoryItemData)