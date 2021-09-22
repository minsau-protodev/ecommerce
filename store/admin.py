from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'created_date', 'modified_date', 'is_available')
    list_filter = ('is_available', 'created_date', 'modified_date')
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('product_name',)
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)