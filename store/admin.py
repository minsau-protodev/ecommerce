from django.contrib import admin
from .models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'created_date', 'modified_date', 'is_available')
    list_filter = ('is_available', 'created_date', 'modified_date')
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('product_name',)
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'created_date', 'is_active')
    list_filter = ('variation_category', 'created_date')
    list_editable = ('is_active', )
    search_fields = ('variation_value',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)